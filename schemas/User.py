from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    address: str
    role: str


class UserUpdate(BaseModel):
    username:str
    email:str
    phone:str
    address:str
    role:str