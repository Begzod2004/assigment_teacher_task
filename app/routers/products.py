from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ProductCreate, ProductResponse
from app.services import create_product, get_products, update_product, delete_product
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"], 
)

# Mahsulot qo'shish
@router.post("/", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db)

# Mahsulotlarni olish
@router.get("/", response_model=list[ProductResponse])
def get_products_endpoint(db: Session = Depends(get_db)):
    return get_products(db)

# Mahsulotni yangilash
@router.put("/{id}", response_model=ProductResponse)
def update_product_endpoint(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    return update_product(id, product, db)

# Mahsulotni o'chirish
@router.delete("/{id}")
def delete_product_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_product(id, db)

