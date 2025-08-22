from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from faker import Faker
from dependencies import get_db, get_api_key, get_current_user
from models.product import Product
from models.user import User

router = APIRouter(prefix="/products", tags=["products"])
fake = Faker()

@router.get("/")
def list_products(page: int = 1, limit: int = 20, api_key = Depends(get_api_key), db: Session = Depends(get_db)):
    if len(api_key.products) == 0:
        for _ in range(1000):
            product = Product(
                name=fake.word().title(),
                description=fake.text(max_nb_chars=200),
                brand=fake.company(),
                quantity=fake.random_int(min=1, max=500),
                price=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
                category=fake.word(),
                photo=f"https://picsum.photos/seed/{fake.uuid4()}/500/500",
                api_key=api_key
            )
            db.add(product)
        db.commit()

    total_items = db.query(Product).filter(Product.api_key == api_key).count()
    total_pages = (total_items + limit - 1) // limit

    products = (
        db.query(Product)
        .filter(Product.api_key == api_key)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
        "items": products
    }

@router.post("/")
def create_product(product: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create products")
    new_product = Product(**product, api_key=current_user.api_key)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.delete("/{id}")
def delete_product(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete products")
    product = db.query(Product).filter(Product.id == id, Product.api_key == current_user.api_key).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}

@router.put("/{id}")
def update_product(id: int, updated_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Only admin or manager can update products")
    product = db.query(Product).filter(Product.id == id, Product.api_key == current_user.api_key).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product
