from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Category
from PYD.categories import CategoryCreate,CategoryReturn, CategoryUpdate

router=APIRouter(prefix='/api/categories', tags=['categories'])

@router.get('/', response_model=List[CategoryReturn])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()