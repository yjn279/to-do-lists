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
    owner_id: int

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str


class User(BaseModel):
    id: int
    name: str
    email: str
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
