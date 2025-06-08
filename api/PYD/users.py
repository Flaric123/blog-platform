from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserReturn(UserBase):
    id:int
    role: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    ...

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[str]