import uuid
from typing import Literal, Type

import jwt
from sqlalchemy.orm import Session

import models
import schemas
from models import User
from settings import JWT_SECRET


def get_users(db: Session) -> list[Type[User]]:
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.User) -> models.User:
    token = jwt.encode(user.model_dump(), JWT_SECRET, algorithm='HS256')
    session = models.FakeSession(token=token)
    role = db.query(models.Role).filter_by(type=user.role.type).one()
    db_user = models.User(name=user.name,
                          email=user.email,
                          role=role,
                          session=session)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_sample(db: Session, type_: Literal['regular', 'admin']) -> models.User:
    id_ = str(uuid.uuid4())[:4]
    role = schemas.Role(type=type_)
    user = schemas.User(
        email=f'{type_}_{id_}@email.com',
        name=f'{type_}_{id_}',
        role=role)
    return create_user(db, user)
