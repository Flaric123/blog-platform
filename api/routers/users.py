from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User
from PYD.users import UserReturn, UserCreate, UserUpdate

router=APIRouter(prefix='/api/users', tags=['Users'])

@router.get('/', response_model=List[UserReturn])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()