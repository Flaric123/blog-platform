from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
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
    category_ids: List[int] = []

class ArticleUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    status: Optional[ArticleStatus]
    category_ids: Optional[List[int]]