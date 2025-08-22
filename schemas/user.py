from pydantic import BaseModel, EmailStr
from typing import Optional

# ---------------- Base ----------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    role: Optional[str] = "customer"

# ---------------- Create ----------------
class UserCreate(UserBase):
    password: str

# ---------------- Update ----------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

# ---------------- Response ----------------
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
