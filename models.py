from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Numeric,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Integer

# Base object which will contain all proto table declarations
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column('phone', String(10))
    active = Column('active', Boolean)
    notification_method = Column('notification_method', String)

    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(64))
    active = Column('active', Boolean)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="activities")
    constraints = relationship("Constraint", back_populates="activity")


class Constraint(Base):
    __tablename__ = 'constraints'
    id = Column(Integer, primary_key=True)
    metric = Column('metric', String(64))
    minimum_value = Column('minimum_value', Numeric)
    maximum_value = Column('maximum_value', Numeric)

    activity_id = Column(Integer, ForeignKey('activities.id'))

    activity = relationship("Activity", back_populates="constraints")
    responses = relationship("Response", back_populates="constraint")


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    response = Column('phone', String)
    date = Column('active', DateTime)

    constraint_id = Column(Integer, ForeignKey('constraints.id'))

    constraint = relationship("Constraint", back_populates="responses")