from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class TaskGet(BaseModel):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    id: int
    title: str


class TaskDelete(BaseModel):
    id: int


class UserGet(BaseModel):
    id: int
    name: str
    email: str
    tasks: list[TaskGet] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    id: int
    name: str
    email: str
    password: str


class UserDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True
