from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Comment, User, Article
from PYD.comments import *
from auth import get_current_user
from auth import is_admin

router = APIRouter(tags=['Comments'])

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
def delete_comment(comment_id: int,user: Annotated[UserReturn, Depends(get_current_user)],db:Session = Depends(get_db)):
    comment=db.query(Comment).filter(Comment.id==comment_id).first()
    if not comment:
        raise HTTPException(404, 'Комментария с таким id не найдено')
    if not is_admin(user.role) or comment.user_id!=user.id:
        raise HTTPException(401, detail="You don't have enough permissions")  
    
    db.delete(comment)
    db.commit()

    return comment

@router.post('/', response_model=CommentReturn)
def create_comment(createData: CommentCreate,user: Annotated[UserReturn, Depends(get_current_user)],db:Session = Depends(get_db)):
    article=db.query(Article).filter(Article.id==createData.article_id).first()

    if not article:
        raise HTTPException(400, "Не удалось найти статью по указанному id")
    
    comment=Comment(**createData.model_dump(exclude={'user_id'}))
    comment.user=user
    comment.article=article

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

@router.put('/{comment_id}', response_model=CommentReturn)
def update_comment(comment_id:int, updateData: CommentUpdate,user: Annotated[UserReturn, Depends(get_current_user)],db:Session = Depends(get_db)):
    comment=db.query(Comment).filter(Comment.id==comment_id).first()

    if not comment:
        raise HTTPException(404, 'Комментария с таким id не найдено')
    if not is_admin(user.role) or comment.user_id!=user.id:
        raise HTTPException(401, detail="You don't have enough permissions")
    
    for field,value in updateData.model_dump().items():
        if value != None:
            setattr(comment, field, value)

    db.commit()
    db.refresh(comment)

    return comment