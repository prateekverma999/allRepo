from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    name: str
    age: int
    city: str
    published: bool = True
    rating: Optional[int] = None

class PostUpdate(PostCreate):
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    published: Optional[bool] = None