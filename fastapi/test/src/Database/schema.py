from pydantic import BaseModel, ConfigDict
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

class PostResponce(BaseModel):
    name: str
    age: int
    city: str
    published: bool = True

    model_config = ConfigDict(from_attributes=True) # for pydantic version 2.0
    # class Config: # for pydantic version 1.0
    #     orm_mode = True