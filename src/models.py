# pylint: disable=C0114, R0903
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

import database


class User(database.Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)

    games = relationship("Game", back_populates="owner")


class Game(database.Base):
    """Game moddel."""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="games")
