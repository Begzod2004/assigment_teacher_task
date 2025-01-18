from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Product, Order, OrderDetail
from app.schemas import UserResponse, ProductResponse, OrderResponse, ProductCreate
from app.dependencies import admin_required

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    users = db.query(User).all()
    return users

@router.get("/products", response_model=List[ProductResponse])
async def get_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    products = db.query(Product).all()
    return products

@router.post("/products", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/orders", response_model=List[OrderResponse])
async def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    orders = db.query(Order).all()
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/stats")
async def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    total_users = db.query(User).count()
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders
    }




    