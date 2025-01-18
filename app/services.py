from sqlalchemy.orm import Session
from app.models import User, Product, Category, Order, OrderDetail
from app.schemas import UserCreate, ProductCreate, CategoryCreate, OrderCreate
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        address=user.address,
        password=hashed_password,
        role=user.role.value  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# PRODUCTS
def create_product(product: ProductCreate, db: Session):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(product_id: int, product_data: ProductCreate, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}

# CATEGORIES
def create_category(category: CategoryCreate, db: Session):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(Category).all()

def delete_category(category_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}

# ORDERS
def create_order(order: OrderCreate, db: Session):
    db_order = Order(customer_id=order.customer_id)
    db.add(db_order)
    db.commit()

    order_detail = OrderDetail(
        order_id=db_order.id,
        product_id=order.product_id,
        quantity=order.quantity
    )
    db.add(order_detail)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()
    
def delete_order(order_id: int, db: Session):
    order = get_order_by_id(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}
