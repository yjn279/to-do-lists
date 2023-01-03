from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    owner_id: int
    created: datetime
    edited: datetime

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str
    done: bool


class User(BaseModel):
    id: int
    name: str
    email: str
    tasks: list[Task] = []
    created: datetime
    edited: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
