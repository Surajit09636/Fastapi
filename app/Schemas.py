from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class UserOut(BaseModel):
    id : int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)
    
class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    model_config = ConfigDict(from_attributes=True)
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: int | None = None
