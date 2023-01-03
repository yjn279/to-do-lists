from sqlalchemy.orm import Session

from . import models, schemas


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(
    db: Session,
    user_id: int,
) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(
    db: Session,
    email: str,
) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(
    db: Session,
    user: schemas.UserCreate,
) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session,
    user_id: int,
    user: schemas.UserCreate,
) -> models.User:
    db_user = get_user(db=db, user_id=user_id)
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(
    db: Session,
    user_id: int,
) -> models.User:
    db_user = get_user(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_tasks_by_owner_id(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, task_id: int) -> models.Task:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_task_by_owner_id(
    db: Session, task_id: int, owner_id: int
) -> models.Task:
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id and models.Task.owner_id == owner_id)
        .first()
    )


def create_task(
    db: Session,
    owner_id,
    task: schemas.TaskCreate,
) -> models.Task:
    db_task = models.Task(**task.dict(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session,
    task_id: int,
    owner_id: int,
    task: schemas.TaskCreate,
) -> models.Task:
    db_task = get_task(db=db, task_id=task_id)
    db_task.title = task.title
    db_task.owner_id = owner_id
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> models.Task:
    db_task = get_task(db=db, task_id=task_id)
    db.delete(db_task)
    db.commit()
    return db_task
