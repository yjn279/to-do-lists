from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("tasks.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    parent = relationship("Task", back_populates="children")
    children = relationship("Task", back_populates="parent")
    owner = relationship("User", back_populates="tasks")
