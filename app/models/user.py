from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_admin: bool = False
    created_at: Union[datetime, str]
    last_login: Optional[Union[datetime, str]] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
