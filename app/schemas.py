from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Post Request - Handling data sent by user to us
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    # because they are the same
    pass

# Post Response - Handling data from us back to the user
class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
# -------------------------------------------------------------------------

# Create User Request - Handling info sent by user, to create a User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Create User Response - Handling user's info from us back to the user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
# -------------------------------------------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str
# -------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]



# 16 Schema Validation with Pydantic Library
'''# Post class is our schema, defining the shape of our Request - We have NOT defined a Schema for our Response yet
class Post(BaseModel):
    title: str
    content: str
    published: bool = True'''