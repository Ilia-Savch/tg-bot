from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    text: Optional[str] = Field(default=None)
    
class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    created_at: datetime


class PostUpdatePartial(BaseModel):
    title: str | None = None
    text: str | None = None
