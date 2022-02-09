from datetime import datetime
from re import L
from typing import Optional
from importlib_metadata import email
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class ResponseCreatuser(BaseModel):
    id: int
    email: str
    created_at: datetime
    # user_id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool= False


class CreatePost(PostBase):
    pass


class ResponceBack(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: ResponseCreatuser

    class Config:
        orm_mode = True


class GetResponseBackOut(BaseModel):
    Post: ResponceBack
    votes: int

    class Config:
        orm_mode = True


class LoginFormate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: str