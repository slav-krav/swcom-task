import jwt
from sqlalchemy.orm import Session

import models
import schemas
from settings import JWT_SECRET


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.User):
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
