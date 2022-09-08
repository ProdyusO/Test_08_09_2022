# pylint: disable=C0114, E0611, R0903
from pydantic import BaseModel, Field


class UserCreateScheme(BaseModel):
    """Pydantic model to create user."""

    name: str
    age: int = Field(ge=1, le=100)
    email: str
    password: str

    class Config:
        """Switch on ORM mode for reading from database."""
        orm_mode = True


class UserSchemeForAuth(UserCreateScheme):
    """Pydantic model to login."""

    id: int

    class Config:
        """Switch on ORM mode for reading from database."""
        orm_mode = True


class GameCreateScheme(BaseModel):
    """Pydantic model for creation game by current user."""

    name: str

    class Config:
        """Switch on ORM mode for reading from database."""
        orm_mode = True


class ShowAllGamesScheme(GameCreateScheme):
    """Pydantic model to show current user's games."""

    id: str
    owner_id: str

    class Config:
        """Switch on ORM mode for reading from database."""
        orm_mode = True
