from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database import get_db
from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserUpdate, User as UserSchema

router = APIRouter(prefix="/users", tags=["users"])

# 1. Create User
@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username or mobile already exists
    exists = db.query(UserModel).filter(
        (UserModel.username == user_data.username) | 
        (UserModel.mobile_e164 == user_data.mobile_e164)
    ).first()
    
    if exists:
        raise HTTPException(status_code=400, detail="Username or Mobile already exists")

    db_user = UserModel(**user_data.model_dump())
    db_user.role = "user"  # Default role
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 2. List All Users
@router.get("/", response_model=List[UserSchema])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(UserModel).offset(skip).limit(limit).all()

# 3. Get Single User
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 4. Update User
@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: uuid.UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user
