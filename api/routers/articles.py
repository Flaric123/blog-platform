from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from typing import List, Optional
from database import get_db
from models import Article, Category, User
from PYD.articles import ArticleReturn, ArticleCreate, ArticleUpdate

router=APIRouter(prefix='/api/posts', tags=['articles'])

@router.get('/', response_model=List[ArticleReturn])
def get_all_articles(db: Session = Depends(get_db),
                     page: Optional[int]=Query(None),
                     limit: Optional[int] = Query(10, ge=1, le=100),
                     category: Optional[str]=Query(None),
                     status: Optional[str]=Query(None)):
    return db.query(Article).all()

@router.get('/{article_id}', response_model=ArticleReturn)
def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    
    return article

@router.post('/', response_model=ArticleReturn)
def create_article(createData : ArticleCreate, db: Session = Depends(get_db)):
    categories=db.query(Category).filter(Category.id.in_(createData.category_ids)).all()
    user=db.query(User).filter(User.id == createData.author_id).first()

    if len(categories) != len(createData.category_ids):
        raise HTTPException(400, "Не удалось найти категории по указанным id")
    if not user:
        raise HTTPException(400, "Не удалось найти пользователя по указанному id")

    article=Article(**createData.model_dump())
    article.categories=categories
    article.author=user

    db.add(article)
    db.commit()
    db.refresh(article)

    return article

@router.put('/{article_id}', response_model=ArticleReturn)
def update_article(article_id:int, updateData: ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    
    for field,value in updateData.model_dump().items():
        if value != None:
            setattr(article, field, value)

    if updateData.category_ids:
        categories = db.query(Category).filter(Category.id.in_(updateData.category_ids)).all()

        if len(categories) != len(updateData.category_ids):
            raise HTTPException(400, 'Не удалось найти категории по указанным id')
        
        article.categories=categories

    db.commit()
    db.refresh(article)

    return article

@router.delete('/{article_id}', response_model=ArticleReturn)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db.expire_on_commit=False

    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")

    db.delete(article)
    db.commit()

    return article