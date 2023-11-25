from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role: Mapped["Role"] = relationship("Role", back_populates="users")
    session: Mapped["FakeSession"] = relationship("FakeSession", back_populates="user")


class FakeSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="session")

