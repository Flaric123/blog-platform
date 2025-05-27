from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryReturn(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class CategoryCreate(CategoryBase):
    ...

class CategoryUpdate(CategoryBase):
    name: Optional[str]