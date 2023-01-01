import os
from datetime import datetime, timedelta
from typing import Union

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import crud, models, schemas
from .database import SessionLocal, engine

load_dotenv(".env")
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")
access_token_expire_minutes = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect id or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=list[schemas.UserGet])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/users/", response_model=schemas.UserGet)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/me/", response_model=schemas.UserGet)
async def read_users_me(
    current_user: schemas.UserGet = Depends(get_current_user),
):
    return current_user


@app.get("/users/{user_id}", response_model=schemas.UserGet)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)


@app.put("/users/{user_id}", response_model=schemas.UserGet)
async def update_user(
    user_id,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return crud.update_user(db, user_id=user_id, user=user)


@app.delete("/users/{user_id}", response_model=schemas.UserGet)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


@app.get("/tasks/", response_model=list[schemas.TaskGet])
async def read_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    user_id = 1
    return crud.get_tasks(db, owner_id=user_id, skip=skip, limit=limit)


@app.post("/tasks/", response_model=schemas.TaskGet)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    user_id = 1
    return crud.create_task(db=db, task=task, user_id=user_id)


@app.get("/tasks/{task_id}", response_model=schemas.TaskGet)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    # user_id = 1
    return crud.get_task(db, task_id=task_id)


@app.put("/tasks/{task_id}", response_model=schemas.TaskGet)
async def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    user_id = 1
    return crud.update_task(db, task_id=task_id, task=task, user_id=user_id)


@app.delete("/tasks/{task_id}", response_model=schemas.TaskGet)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    # user_id = 1
    return crud.delete_task(db, task_id=task_id)
