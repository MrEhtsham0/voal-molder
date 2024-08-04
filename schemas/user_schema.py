from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserInput(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    join_date: datetime

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class AuthInput(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class AuthOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        from_attributes = True