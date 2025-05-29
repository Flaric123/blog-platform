from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Comment, User, Article
from PYD.comments import *

router = APIRouter(prefix='/api/comments', tags=['Comments'])

@router.get('/', response_model=List[CommentReturn])
def get_all_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()

@router.get('/{comment_id}', response_model=CommentReturn)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment=db.query(Comment).filter(Comment.id==comment_id)

    if not comment:
        raise HTTPException(404, 'Комментария с таким id не найдено')

    return comment

@router.delete('/{comment_id}', response_model=CommentReturn)
def delete_comment(comment_id: int, db:Session = Depends(get_db)):
    comment=db.query(Comment).filter(Comment.id==comment_id)

    if not comment:
        raise HTTPException(404, 'Комментария с таким id не найдено')
    
    db.delete(comment)
    db.commit()

    return comment

@router.post('/', response_model=CommentReturn)
def create_comment(createData: CommentCreate,db:Session = Depends(get_db)):
    user=db.query(User).filter(User.id==createData.user_id).first()
    article=db.query(Article).filter(Article.id==createData.article_id).first()

    if not user:
        raise HTTPException(400, "Не удалось найти пользователя по указанному id")
    if not article:
        raise HTTPException(400, "Не удалось найти статью по указанному id")
    
    comment=Comment(**createData.model_dump())
    comment.user=user
    comment.article=article

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

@router.put('/{comment_id}', response_model=CommentReturn)
def update_comment(comment_id:int, updateData: CommentUpdate, db:Session = Depends(get_db)):
    comment=db.query(Comment).filter(Comment.id==comment_id).first()

    if not comment:
        raise HTTPException(404, 'Комментария с таким id не найдено')
    
    for field,value in updateData.model_dump().items():
        if value != None:
            setattr(comment, field, value)

    db.commit()
    db.refresh(comment)

    return comment