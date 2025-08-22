from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db, get_api_key
from models.user import User
from utils.security import verify_password, hash_password
from utils.auth import create_access_token
from schemas.user import UserCreate, UserResponse
from schemas.auth import AuthLogin, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# -------- REGISTER --------
@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    api_key = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    # Força sempre role=customer
    user = User(
        name=user_data.name,
        email=user_data.email,
        address=user_data.address,
        password=hash_password(user_data.password),
        role="customer",
        api_key=api_key
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# -------- LOGIN --------
@router.post("/login", response_model=AuthResponse)
def login(
    login_data: AuthLogin,
    api_key = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
