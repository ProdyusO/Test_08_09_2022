# pylint: disable=C0114, C0410, C0103
from sqlalchemy.orm import Session

import models, schemas


def get_user_by_email(db: Session, email: str):
    """Gives user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreateScheme):
    """Writes new user to database."""
    db_user = models.User(name=user.name, age=user.age, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_name(db: Session, username):
    """Gives user by name."""
    return db.query(models.User).filter(models.User.name == username).first()


def write_current_user(game1, db: Session, current_user):
    """Writes current user to database."""
    detail = db.query(models.User).filter(models.User.name == current_user).first()
    db_game = models.Game(**game1.dict(), owner_id=detail.id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_games(db: Session, skip: int = 0, limit: int = 100):
    """Gives all games from database."""
    return db.query(models.Game).offset(skip).limit(limit).all()


def get_current_game(db, current_user):
    """Shows all current user's games."""
    user = db.query(models.User).filter(models.User.name == current_user).first()
    return db.query(models.Game).filter(models.Game.owner_id == user.id).all()
