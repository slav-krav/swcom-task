from __future__ import annotations

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import crud
import models
from database import SessionLocal, create_tables, get_or_create
from opa_middleware import opa_access_check
from schemas import User, UserWithToken

app = FastAPI()
API_ENDPOINT = '/api/users'

app.middleware('http')(opa_access_check)

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def init(db: Session = Depends(get_db)):
    """Issue a simple get request here to populate database with initial entities."""
    create_tables(db.connection())
    get_or_create(db, models.Role, type='admin')
    get_or_create(db, models.Role, type='regular')
    return {'Tables created': True}


@app.get(API_ENDPOINT)
def read_users(db: Session = Depends(get_db),
               show_jwt: bool = False,
               auth: str = Depends(security)) -> list[User] | list[UserWithToken]:
    users = crud.get_users(db)
    if not show_jwt:
        return [User.model_validate(user) for user in users]

    return [UserWithToken.model_validate(user) for user in users]


@app.post(API_ENDPOINT)
def create_user(user: User, db: Session = Depends(get_db), auth: str = Depends(security)) -> UserWithToken:
    user = crud.create_user(db, user)
    return UserWithToken.model_validate(user)
