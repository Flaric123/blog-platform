from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
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
    article_id: Annotated[int, Field(exclude=True)]
    user_id: Annotated[int, Field(exclude=True)]

class CommentUpdate(CommentBase):
    content: Optional[str]=None