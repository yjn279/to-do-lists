from pydantic import BaseModel


class TaskGet(BaseModel):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    owner_id: int


class TaskUpdate(BaseModel):
    id: int
    title: str
    owner_id: int


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
