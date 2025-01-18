from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import *
from app.schemas import *
from app.database import get_db
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.schemas import UserResponse, UserRole
from app.services import create_user

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user_endpoint(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    address: str = Form(None),
    password: str = Form(...),
    role: UserRole = Form(UserRole.customer),  # Default to "Customer"
    db: Session = Depends(get_db)
):
    user_data = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "address": address,
        "password": password,
        "role": role
    }
    return create_user(UserCreate(**user_data), db)

# Get all users
@router.get("/users", response_model=list[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

# Delete a user
@router.delete("/users/{id}")
def delete_user_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_user(id, db)

# PRODUCT ROUTES
@router.post("/products", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db)

@router.get("/products", response_model=List[ProductResponse])
def get_products_endpoint(db: Session = Depends(get_db)):
    return get_products(db)

@router.put("/products/{id}", response_model=ProductResponse)
def update_product_endpoint(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    return update_product(id, product, db)

@router.delete("/products/{id}")
def delete_product_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_product(id, db)

# CATEGORY ROUTES
@router.post("/categories", response_model=CategoryResponse)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(category, db)

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories_endpoint(db: Session = Depends(get_db)):
    return get_categories(db)

@router.delete("/categories/{id}")
def delete_category_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_category(id, db)

# ORDER ROUTES
@router.post("/orders", response_model=OrderResponse)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(order, db)

@router.get("/orders", response_model=List[OrderResponse])
def get_orders_endpoint(db: Session = Depends(get_db)):
    return get_orders(db)

@router.delete("/orders/{id}")
def delete_order_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_order(id, db)
