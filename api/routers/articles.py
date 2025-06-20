from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from typing import List, Optional, Annotated
from database import get_db
from models import Article, Category, User, ArticleStatus
from PYD.articles import ArticleReturn, ArticleCreate, ArticleUpdate
from sqlalchemy.sql import text
from PYD.users import UserReturn
from auth import RoleChecker
from auth import is_admin
import enum
from sqlalchemy import Enum, func

router=APIRouter(tags=['articles'])

class SortOrder(enum.Enum):
    asc='asc'
    desc='desc'

@router.get('/', response_model=List[ArticleReturn])
def get_all_articles(db: Session = Depends(get_db),
                     page: int=Query(ge=1,example=1),
                     limit: int = Query(ge=1, le=100, example=2),
                     category: Optional[str]=Query(None),
                     status: Optional[ArticleStatus]=Query(None),
                     sort_by_popularity: Optional[SortOrder]=Query(None)):
    articles=db.query(Article)
    if category!=None:
        db_category=db.query(Category).filter(Category.name==category).first()
        if not db_category:
            raise HTTPException(404, "Категория с таким имененем не найдена")
        articles=articles.filter(Article.categories.contains(db_category))

    if status!=None:
        articles=articles.filter(Article.status==status)

    min_offset=(page-1)*limit
    if sort_by_popularity!=None:
        if sort_by_popularity==SortOrder.desc:
            articles=articles.order_by(Article.likes_count.desc())
        else:
            articles=articles.order_by(Article.likes_count)
    paginated_articles=articles.offset(min_offset).limit(limit).all()

    return paginated_articles

@router.get('/{article_id}', response_model=ArticleReturn)
def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    
    return article

@router.post('/', response_model=ArticleReturn)
def create_article(createData : ArticleCreate,user: Annotated[UserReturn, Depends(RoleChecker(allowed_roles=['author','admin']))],db:Session = Depends(get_db)):
    categories=db.query(Category).filter(Category.id.in_(createData.category_ids)).all()

    if len(categories) != len(createData.category_ids):
        raise HTTPException(400, "Не удалось найти категории по указанным id")
    
    article=Article(**createData.model_dump(exclude={'user_id'}))
    article.categories=categories
    article.author=user

    article.last_changed_by_user_id=user.id

    db.add(article)
    db.commit()
    db.refresh(article)

    return article

@router.put('/{article_id}', response_model=ArticleReturn)
def update_article(article_id:int, updateData: ArticleUpdate,user: Annotated[UserReturn, Depends(RoleChecker(allowed_roles=['author','admin']))],db:Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    if not is_admin(user.role) and article.author_id!=user.id:
        raise HTTPException(401, detail="У вас недостаточно прав")
    
    for field,value in updateData.model_dump().items():
        if value != None:
            setattr(article, field, value)

    if updateData.category_ids:
        categories = db.query(Category).filter(Category.id.in_(updateData.category_ids)).all()

        if len(categories) != len(updateData.category_ids):
            raise HTTPException(400, 'Не удалось найти категории по указанным id')
        
        article.categories=categories

    article.last_changed_by_user_id=user.id

    db.commit()
    db.refresh(article)

    return article

@router.delete('/{article_id}', response_model=ArticleReturn)
def delete_article(article_id: int,user: Annotated[UserReturn, Depends(RoleChecker(allowed_roles=['author','admin']))],db:Session = Depends(get_db)):
    db.expire_on_commit=False

    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    if not is_admin(user.role) and article.author_id!=user.id:
        raise HTTPException(401, detail="У вас недостаточно прав")

    db.delete(article)
    db.commit()

    return article