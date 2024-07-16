#!/usr/bin/env python3
'''Module defines SQLAlchemy model `User`'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    '''Mapper to a DB table'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)
