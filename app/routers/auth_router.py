from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import Token, UserCreate, UserResponse
from app.models import User
from app.auth import authenticate_user, create_access_token, hash_password
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        address=user.address,
        password=hashed_password,
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # grant_type tekshirish
    if form_data.grant_type and form_data.grant_type != "password":
        raise HTTPException(
            status_code=400,
            detail="Unsupported grant type"
        )

    async def get_user(username: str):
        return db.query(User).filter(User.username == username).first()
    
    user = await authenticate_user(form_data.username, form_data.password, get_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "scopes": form_data.scopes or []
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
