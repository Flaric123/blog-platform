from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
from PYD.categories import CategoryReturn
from PYD.users import UserReturn
from PYD.comments import CommentReturn

class ArticleStatus(str, Enum):
    draft = "draft"
    published = "published"

class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleReturn(ArticleBase):
    id: int
    author: UserReturn
    status: ArticleStatus
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryReturn]
    comments: List[CommentReturn]

    class Config:
        orm_mode = True

class ArticleCreate(ArticleBase):
    status: ArticleStatus = ArticleStatus.draft
    author_id: Annotated[int, Field(exclude=True)]
    category_ids: Annotated[List[int], Field(exclude=True)] = []

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str]= None
    status: Optional[ArticleStatus]= None
    category_ids: Optional[List[int]]= None