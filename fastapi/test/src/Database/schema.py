from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


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

    # model_config = ConfigDict(from_attributes=True) # for pydantic version 2.0
    # class Config: # for pydantic version 1.0
    #     orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserCreate(UserLogin):
    pass

class UserResponce(BaseModel):
    email: EmailStr
    created_at: datetime