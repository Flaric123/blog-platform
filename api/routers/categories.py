from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Category
from PYD.categories import CategoryCreate,CategoryReturn, CategoryUpdate

router=APIRouter(tags=['categories'])

@router.get('/', response_model=List[CategoryReturn])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get('/{category_id}', response_model=CategoryReturn)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(404, "Категория с таким id не найдена")
    
    return category

@router.delete('/{category_id}', response_model=CategoryReturn)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(404, "Категория с таким id не найдена")

    db.delete(category)
    db.commit()

    return category

@router.put('/{category_id}', response_model=CategoryReturn)
def update_category(updateData: CategoryUpdate, category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(404, "Категория с таким id не найдена")
    
    for field,value in updateData.model_dump().items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category

@router.post('/', response_model=CategoryReturn)
def create_category(createData: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**createData.model_dump())

    db.add(category)
    db.commit()

    return category