from pydantic import BaseModel, EmailStr

# -------- Login --------
class AuthLogin(BaseModel):
    email: EmailStr
    password: str

# -------- Login Response --------
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
