from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, computed_field

class LikeReturn(BaseModel):
    id: int
    user_id: int
    article_id:int
    created_at: datetime