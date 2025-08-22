from fastapi import FastAPI
from database import Base, engine
from routers import product, user, auth, api_key

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(api_key.router)

@app.get("/")
def root():
    return {"message": "API is working"}
