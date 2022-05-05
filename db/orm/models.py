from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Numeric,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql import expression, func
from sqlalchemy.types import Boolean, Integer

# Base object which will contain all proto table declarations
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone = Column('phone', String(10))
    active = Column('active', Boolean)
    notification_method = Column('notification_method', String)

    activities = relationship("Activity")


class Activity(Base):
    __tablename__ = 'activitys'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(64))
    description = Column('description', String(256))
    frequency = Column('frequency', Integer)
    active = Column('active', Boolean)

    user_id = Column(Integer, ForeignKey('users.id'))

    constraints = relationship("Constraint")


class Constraint(Base):
    __tablename__ = 'constraints'
    id = Column(Integer, primary_key=True)
    metric = Column('metric', String(64))
    minimum_value = Column('minimum_value', Numeric)
    maximum_value = Column('maximum_valuoe', Numeric)

    activity_id = Column(Integer, ForeignKey('activitys.id'))

    responses = relationship("Response")


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    response = Column('phone', String)
    date = Column('active', DateTime)

    constraint_id = Column(Integer, ForeignKey('constraints.id'))