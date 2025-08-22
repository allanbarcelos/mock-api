from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(64), unique=True, index=True)

    products = relationship("Product", back_populates="api_key", cascade="all, delete-orphan")
    users = relationship("User", back_populates="api_key", cascade="all, delete-orphan")
