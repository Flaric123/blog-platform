from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from database import get_db
from models import Article, Like
from PYD.likes import *
from PYD.users import UserReturn
from auth import get_current_user

router=APIRouter(tags=['likes'])

@router.post('/{article_id}', response_model=LikeReturn)
def create_like(article_id:int, user: Annotated[UserReturn,Depends(get_current_user)], db: Session=Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    
    like=Like(user_id=user.id,article_id=article.id)

    db.add(like)
    db.commit()

    return like

@router.delete('/{article_id}', response_model=LikeReturn)
def delete_like(article_id:int, user: Annotated[UserReturn,Depends(get_current_user)], db: Session=Depends(get_db)):
    article=db.query(Article).filter(Article.id==article_id).first()

    if not article:
        raise HTTPException(404, 'Категории с таким именем нет')

    like=db.query(Like).filter(Like.article_id==article_id and Like.user_id==user.id).first()

    if not like:
        raise HTTPException(404, 'Вы не оставляли лайк под данной статьёй')
    
    db.delete(like)
    db.commit()

    return like

@router.get('/', response_model=List[LikeReturn])
def get_user_likes(user: Annotated[UserReturn,Depends(get_current_user)], db: Session=Depends(get_db)):
    return db.query(Like).filter(Like.user_id==user.id).all()