from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.auth import hash_password
from app.models import User
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Foydalanuvchining username yoki emaili takrorlanmasligini tekshirish
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Parolni hash qilish
    hashed_password = hash_password(user.password)

    # Foydalanuvchini saqlash
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        address=user.address,
        password=hashed_password,
        role=user.role.value
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.auth import authenticate_user, create_access_token
from app.schemas import Token
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Foydalanuvchini autentifikatsiya qilish
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # JWT token yaratish
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
