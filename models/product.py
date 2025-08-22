from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(500))
    brand = Column(String(100))
    quantity = Column(Integer)
    price = Column(Float)
    category = Column(String(100))
    photo = Column(String(255))
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    api_key = relationship("APIKey", back_populates="products")
