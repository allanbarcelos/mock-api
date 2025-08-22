from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    address = Column(String(500))
    password = Column(String(255))
    role = Column(String(50), default="customer")
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    api_key = relationship("APIKey", back_populates="users")
