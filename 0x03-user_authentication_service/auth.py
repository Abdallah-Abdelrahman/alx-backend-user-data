#!/usr/bin/env python3
'''Module defines `_hash_password` function'''
from typing import Union
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    '''returns bytes is a salted hash of the input password'''
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''generate uuid'''
    return str(uuid.uuid4())


class Auth:
    '''Auth class to interact with the authentication database.
    '''

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
            return self._db.add_user(email, psw)

    def valid_login(self, email: str, password: str) -> bool:
        '''Locating the user by email'''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''Find the user corresponding to the email,
        generate a new UUID and store it in the database,
        as the user’s session_id
        '''
        try:
            user = self._db.find_user_by(email=email)
            uuid_ = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=uuid_)
            return uuid_

        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''Returns the corresponding User'''
        if not session_id:
            return None
        return self._db.find_user_by(session_id=session_id)
