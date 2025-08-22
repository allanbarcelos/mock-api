from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from faker import Faker
from dependencies import get_db, get_current_user
from models.user import User
from utils.security import hash_password
from schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])
fake = Faker()

# ---------------- LIST ----------------
@router.get("/", response_model=list[UserResponse])
def list_users(
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    api_key = current_user.api_key

    if len(api_key.users) == 0:
        roles_count = {"admin": 1, "manager": 1, "vendor": 3, "customer": 5}
        for role, count in roles_count.items():
            for _ in range(count):
                user = User(
                    name=fake.name(),
                    email=fake.unique.email(),
                    address=fake.address(),
                    password=hash_password("password123"),
                    role=role,
                    api_key=api_key
                )
                db.add(user)
        db.commit()

    users = (
        db.query(User)
        .filter(User.api_key == api_key)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return users

# ---------------- CREATE ----------------
@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_data.role != "customer" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can assign roles")

    user = User(
        name=user_data.name,
        email=user_data.email,
        address=user_data.address,
        password=hash_password(user_data.password),
        role=user_data.role,
        api_key=current_user.api_key
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------------- DELETE ----------------
@router.delete("/{id}")
def delete_user(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")

    user = db.query(User).filter(User.id == id, User.api_key == current_user.api_key).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# ---------------- UPDATE ----------------
@router.put("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    updated_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id, User.api_key == current_user.api_key).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role != "admin" and current_user.id != id:
        raise HTTPException(status_code=403, detail="You can only edit your own profile")

    if updated_data.password:
        user.password = hash_password(updated_data.password)

    for key, value in updated_data.dict(exclude_unset=True).items():
        if key != "password":
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
