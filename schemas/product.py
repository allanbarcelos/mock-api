from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    brand: str
    quantity: int
    price: float
    category: str
    photo: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
