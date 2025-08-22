from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from faker import Faker
import secrets
from dependencies import get_db, get_api_key
from models.api_key import APIKey
from models.user import User
from utils.security import hash_password

router = APIRouter(prefix="/api", tags=["api_key"])
fake = Faker()

@router.get("/")
def create_api_key(db: Session = Depends(get_db)):
    key = secrets.token_hex(16)
    api_key = APIKey(key=key)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    # cria admin padrão
    admin_user = User(
        name="Admin",
        email=fake.unique.email(),
        address="Admin Address",
        password=hash_password("admin123"),
        role="admin",
        api_key=api_key
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return {
        "api_key": api_key.key,
        "admin_user": {
            "id": admin_user.id,
            "name": admin_user.name,
            "email": admin_user.email,
            "password": "admin123"
        }
    }

@router.delete("/")
def delete_api_key(api_key: APIKey = Depends(get_api_key), db: Session = Depends(get_db)):
    db.delete(api_key)
    db.commit()
    return {"message": "API Key deleted"}
