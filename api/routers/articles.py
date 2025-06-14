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

router=APIRouter(prefix='/api/posts', tags=['articles'])

@router.get('/', response_model=List[ArticleReturn])
def get_all_articles(db: Session = Depends(get_db),
                     page: Optional[int]=Query(None,ge=1),
                     limit: Optional[int] = Query(None, ge=1, le=100),
                     category: Optional[str]=Query(None),
                     status: Optional[ArticleStatus]=Query(None)):
    articles=db.query(Article)
    if category!=None:
        db_category=db.query(Category).filter(Category.name==category).first()
        if not db_category:
            raise HTTPException(404, "Категория с таким имененем не найдена")
        articles=articles.filter(Article.categories.contains(db_category))
    if status!=None:
        articles=articles.filter(Article.status==status)
    min_offset=(page-1)*limit
    max_offset=min_offset+limit

    filtered_articles=articles.all()
    paginated_articles=filtered_articles[min_offset:max_offset]

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

    db.add(article)
    db.commit()
    db.refresh(article)

    return article

@router.put('/{article_id}', response_model=ArticleReturn)
def update_article(article_id:int, updateData: ArticleUpdate,user: Annotated[UserReturn, Depends(RoleChecker(allowed_roles=['author','admin']))],db:Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    if not is_admin(user.role) or article.author_id!=user.id:
        raise HTTPException(401, detail="You don't have enough permissions")
    
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
def delete_article(article_id: int,user: Annotated[UserReturn, Depends(RoleChecker(allowed_roles=['author','admin']))],db:Session = Depends(get_db)):
    db.expire_on_commit=False

    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(404, "Статьи с таким id не найдено")
    if not is_admin(user.role) or article.author_id!=user.id:
        raise HTTPException(401, detail="You don't have enough permissions")

    db.delete(article)
    db.commit()

    return article