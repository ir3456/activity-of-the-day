import models
import schemas
from sqlalchemy.orm import Session


# User
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone(db: Session, user_phone: str):
    return db.query(models.User).filter(models.User.phone == user_phone).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Add the user to the database
    db_user = models.User(phone=user.phone, active=user.active)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Activity
def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()


def create_activity(db: Session, activity: schemas.ActivityCreate, user_id: int):
    # Add the activity to the database
    db_activity = models.Activity(name=activity.name, active=activity.active, user_id=user_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


# Cosntraint
def get_constraint(db: Session, constraint_id: int):
    return db.query(models.Constraint).filter(models.constraint.id == constraint_id).first()


def create_constraint(db: Session, constraint: schemas.ConstraintCreate, activity_id: int):
    # Add the constraint to the database
    db_constraint = models.Constraint(
        metric=constraint.metric,
        minimum_value=constraint.minimum_value,
        maximum_value=constraint.maximum_value,
        activity_id=activity_id,
    )
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    return db_constraint


# Cosntraint
def create_response(db: Session, response: schemas.ResponseCreate, constraint_id: int):
    # Add the constraint to the database
    db_response = models.Response(
        name=response.response, minimum_value=response.date, constraint_id=constraint_id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response
