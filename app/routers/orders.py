from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import OrderCreate, OrderResponse
from app.models import Order, OrderDetail
from app.services import create_order, get_orders, delete_order
from app.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],  
)

@router.post("/", response_model=OrderResponse)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(order, db)

@router.get("/", response_model=list[OrderResponse])
def get_orders_endpoint(db: Session = Depends(get_db)):
    return get_orders(db)

@router.delete("/{id}")
def delete_order_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_order(id, db)

@router.get("/me")
def get_my_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    orders = db.query(Order).filter(Order.customer_id == current_user.id).all()
    return orders

@router.get("/{order_id}")
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    customer = order.customer  # Buyurtmani qilgan foydalanuvchi
    order_details = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()

    products = [
        {"product_name": detail.product.name, "quantity": detail.quantity}
        for detail in order_details
    ]

    return {
        "order_id": order.id,   
        "customer_name": customer.full_name,
        "status": order.status,
        "products": products,
    }
