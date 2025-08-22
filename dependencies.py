from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from jwt import DecodeError, ExpiredSignatureError
import jwt
from database import SessionLocal
from models.user import User
from models.api_key import APIKey
from config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_api_key(api_key: str = Header(None, alias="API-Key"), db: Session = Depends(get_db)):
    api_key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not api_key_obj:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_obj

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload.get("user_id")).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
