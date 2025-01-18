from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Order, Product, OrderDetail
from app.schemas import OrderCreate, OrderResponse, ProductResponse
from app.dependencies import customer_required

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@router.get("/products", response_model=List[ProductResponse])
async def view_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(customer_required)
):
    products = db.query(Product).filter(Product.stock_quantity > 0).all()
    return products

@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(customer_required)
):
    orders = db.query(Order).filter(Order.customer_id == current_user.id).all()
    return orders

@router.get("/orders/{order_id}/status")
async def get_order_status(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(customer_required)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.customer_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"status": order.status}

@router.post("/place-order", response_model=OrderResponse)
async def place_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(customer_required)
):
    # Check if products exist and have enough stock
    for order_detail in order.order_details:
        product = db.query(Product).filter(Product.id == order_detail.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {order_detail.product_id} not found")
        if product.stock_quantity < order_detail.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")

    # Create order
    db_order = Order(customer_id=current_user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add order details and update stock
    for order_detail in order.order_details:
        product = db.query(Product).filter(Product.id == order_detail.product_id).first()
        product.stock_quantity -= order_detail.quantity
        
        db_order_detail = OrderDetail(
            order_id=db_order.id,
            product_id=order_detail.product_id,
            quantity=order_detail.quantity
        )
        db.add(db_order_detail)

    db.commit()
    return db_order
