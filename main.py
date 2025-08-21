from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import NoResultFound
from faker import Faker
import secrets

# Configuração MySQL
DATABASE_URL = "mysql+mysqlconnector://sehwugsufzepby:sehwug-sufzEp-byrby0@db4free.net/sehwugsufzepby"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
fake = Faker()

app = FastAPI()

# ------------------ MODELOS -------------------
class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(64), unique=True, index=True)
    products = relationship("Product", back_populates="api_key")


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

# Cria as tabelas
Base.metadata.create_all(bind=engine)

# ------------------ DEPENDÊNCIAS -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_api_key(api_key: str = Header(None), db=Depends(get_db)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Api-Key header is required")
    try:
        return db.query(APIKey).filter(APIKey.key == api_key).one()
    except NoResultFound:
        raise HTTPException(status_code=403, detail="Invalid API Key")


# ------------------ ROTAS -------------------

@app.get("/")
def root():
    return {"message": "API is working"}


@app.get("/api")
def create_api_key(db: SessionLocal = Depends(get_db)):
    key = secrets.token_hex(16)
    api_key = APIKey(key=key)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return {"key": api_key.key}


@app.delete("/api")
def delete_api_key(api_key: APIKey = Depends(get_api_key), db: SessionLocal = Depends(get_db)):
    db.delete(api_key)
    db.commit()
    return {"message": "API Key deleted"}


@app.get("/products")
def list_products(page: int = 1, limit: int = 20, api_key: APIKey = Depends(get_api_key), db: SessionLocal = Depends(get_db)):
    # Se não há produtos vinculados, gerar 1000 mock
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

    products = db.query(Product).filter(Product.api_key == api_key).offset((page-1)*limit).limit(limit).all()
    return products


@app.post("/products")
def create_product(product: dict, api_key: APIKey = Depends(get_api_key), db: SessionLocal = Depends(get_db)):
    new_product = Product(
        name=product.get("name"),
        description=product.get("description"),
        brand=product.get("brand"),
        quantity=product.get("quantity"),
        price=product.get("price"),
        category=product.get("category"),
        photo=product.get("photo"),
        api_key=api_key
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.delete("/products/{id}")
def delete_product(id: int, api_key: APIKey = Depends(get_api_key), db: SessionLocal = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id, Product.api_key == api_key).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


@app.put("/products/{id}")
def update_product(id: int, updated_data: dict, api_key: APIKey = Depends(get_api_key), db: SessionLocal = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id, Product.api_key == api_key).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in updated_data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product
