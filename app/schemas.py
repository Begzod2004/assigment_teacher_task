from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserRole(str, Enum):
    ADMIN = "Admin"
    CUSTOMER = "Customer"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    address: str
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserInDB(UserBase):
    hashed_password: str

class ProductBase(BaseModel):
    name: str
    category_id: int
    sku: str
    description: str
    price: float
    stock_quantity: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class OrderDetailBase(BaseModel):
    product_id: int
    quantity: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailResponse(OrderDetailBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int
    status: str = "Pending"

class OrderCreate(OrderBase):
    order_details: List[OrderDetailCreate]

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    order_details: List[OrderDetailResponse]

    class Config:
        from_attributes = True
