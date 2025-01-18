from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import CategoryCreate, CategoryResponse
from app.services import create_category, get_categories, delete_category
from app.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],  
)

@router.post("/", response_model=CategoryResponse)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(category, db)

@router.get("/", response_model=list[CategoryResponse])
def get_categories_endpoint(db: Session = Depends(get_db)):
    return get_categories(db)

@router.delete("/{id}")
def delete_category_endpoint(id: int, db: Session = Depends(get_db)): 
    return delete_category(id, db)
