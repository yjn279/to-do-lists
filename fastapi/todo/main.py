from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return crud.update_user(db, user_id=user_id, user=user)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


@app.get("/users/{user_id}/tasks/", response_model=list[schemas.Task])
def read_tasks(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_tasks(db, owner_id=user_id, skip=skip, limit=limit)


@app.post("/users/{user_id}/tasks/", response_model=schemas.Task)
def create_task(
    user_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    return crud.create_task(db=db, task=task, user_id=user_id)


@app.get("/users/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def read_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id=task_id)


@app.put("/users/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    user_id: int,
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    return crud.update_task(db, task_id=task_id, task=task, user_id=user_id)


@app.delete("/users/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def delete_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id=task_id)
