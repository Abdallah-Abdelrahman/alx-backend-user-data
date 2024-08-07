#!/usr/bin/env python3
'''DB module
'''
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    '''DB class
    '''

    def __init__(self) -> None:
        '''Initialize a new DB instance
        '''
        self._engine = create_engine('sqlite:///a.db', echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''Memoized session object
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''save the user to the database'''
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kw) -> User:
        ''' returns the first row found in the users table,
        as filtered by the method’s input arguments.

        Raises:
            NoResultFound: if no user found
            InvalidRequestError: wrong query arguments are passed
        '''
        return self._session.query(User).filter_by(**kw).one()

    def update_user(self, user_id: int, **kw: Dict[str, str]):
        '''side effect to udpate a user'''
        user = self.find_user_by(id=user_id)
        if not user:
            return
        for k, v in kw.items():
            if not hasattr(User, k):
                raise ValueError
            setattr(user, k, v)
