from fastapi import Depends, FastAPI, HTTPException
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from . import models, crud, schemas

# Database connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"],
    database=os.environ["POSTGRES_DB"],
)

#
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User Path Operations
@app.post("/users/", response_model=schemas.User)
def create_user(user, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists with that phone number")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/phone/{user_phone}", response_model=schemas.User)
def get_user_by_phone(user_phone: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, user_phone=user_phone)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Activity Path Operations
@app.post("/users/{user_id}/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_activity(db=db, activity=activity, user_id=user_id)


@app.get("/activities/{activity_id}", response_model=schemas.Activity)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_activity(db, activity_id=activity_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_user


# Constraint Path Operations
@app.post("/activities/{activity_id}/constraints/", response_model=schemas.Constraint)
def create_constraint(constraint: schemas.ConstraintCreate, activity_id: int, db: Session = Depends(get_db)):
    return crud.create_constraint(db=db, contraint=constraint, activity_id=activity_id)


@app.get("/constraints/{constraint_id}", response_model=schemas.Constraint)
def get_constraint(constraint_id: int, db: Session = Depends(get_db)):
    db_constraint = crud.get_constraint(db, constraint_id=constraint_id)
    if db_constraint is None:
        raise HTTPException(status_code=404, detail="Constraint not found")
    return db_constraint


# Response Path Operations
@app.post("/constraints/{constraint_id}/response", response_model=schemas.Response)
def create_response(response: schemas.ResponseCreate, constraint_id: int, db: Session = Depends(get_db)):
    return crud.create_response(db=db, response=response, constraint_id=constraint_id)


