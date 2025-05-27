from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserReturn(UserBase):
    id: int
    created_at: datetime
    role: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    ...

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[str]