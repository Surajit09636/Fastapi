from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool
    
    model_config = ConfigDict(from_attributes=True)
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id : int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str