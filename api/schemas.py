from typing_extensions import Literal

from pydantic import BaseModel, ConfigDict


class OrmModelBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Role(OrmModelBase):
    type: Literal['admin', 'regular']


class Session(OrmModelBase):
    token: str


class User(OrmModelBase):
    name: str
    email: str
    role: Role


class UserWithToken(User):
    session: Session
