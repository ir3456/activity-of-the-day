from typing import Optional

from pydantic import BaseModel


# Response
class ResponseBase(BaseModel):
    response: str
    date: str


class ResponseCreate(ResponseBase):
    pass


class Response(ResponseBase):
    id: int
    constraint_id: int

    class Config:
        orm_mode = True


# Cosntraint
class ConstraintBase(BaseModel):
    metric: str
    minimum_value: float
    maximum_value: float


class ConstraintCreate(ConstraintBase):
    pass


class Constraint(ConstraintBase):
    id: int
    activity_id: int
    responses: list[Response] = []

    class Config:
        orm_mode = True


# Activity
class ActivityBase(BaseModel):
    name: str
    active: bool


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    user_id: int
    constraints: list[Constraint] = []

    class Config:
        orm_mode = True


# User
class UserBase(BaseModel):
    phone: str
    active: bool


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    activities: list[Activity] = []

    class Config:
        orm_mode = True
