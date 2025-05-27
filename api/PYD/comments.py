from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from PYD.users import UserReturn

class CommentBase(BaseModel):
    content: str

class CommentReturn(CommentBase):
    id: int
    user: UserReturn
    article_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CommentCreate(CommentBase):
    article_id: int
    user_id: int

class CommentUpdate(CommentBase):
    article_id: Optional[int]
    user_id: Optional[int]
    content: Optional[str]