# pylint: disable=C0114, C0410, C0103
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


models.database.Base.metadata.create_all(bind=engine)


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """Creates database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/games/", response_model=list[schemas.ShowAllGamesScheme])
def get_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get endpoint to receive list of all games and users who connected to this games."""
    return crud.get_games(db, skip=skip, limit=limit)


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Post endpoint to login."""
    user = crud.get_user_by_name(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect name or password")
    password_from_form = form_data.password
    if not password_from_form == user.password:
        raise HTTPException(status_code=400, detail="Incorrect name or password")
    return {"access_token": user.name, "token_type": "bearer"}


@app.post("/user/", response_model=schemas.UserCreateScheme, status_code=201)
def registraion(user: schemas.UserCreateScheme, db: Session = Depends(get_db)):
    """Post endpoint for user creations."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/game/", response_model=schemas.GameCreateScheme, status_code=201)
def connect_to_game(
    game: schemas.GameCreateScheme,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2_scheme)
):
    """ "Post endpoint to game connection."""
    return crud.write_current_user(game1=game, db=db, current_user=current_user)


@app.get("/my_games/", response_model=list[schemas.ShowAllGamesScheme])
async def get_me(db: Session = Depends(get_db), current_user: str = Depends(oauth2_scheme)):
    """Get endpoint to receive info about current user and info about all connected games."""
    return crud.get_current_game(db, current_user)
