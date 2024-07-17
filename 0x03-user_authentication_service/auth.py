#!/usr/bin/env python3
'''Module defines `_hash_password` function'''
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    '''returns bytes is a salted hash of the input password'''
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''Initialize the instance'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Add new user'''
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            psw = _hash_password(password)
            return self._db.add_user(email, str(psw))
