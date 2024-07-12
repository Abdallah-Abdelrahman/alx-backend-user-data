#!/usr/bin/env python3
'''Module defines `SessionExpAuth` class'''
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''class definition'''
    def __init__(self):
        '''initialize the isntance'''
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        '''Create a Session ID '''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''overload parent method'''
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        user_info = self.user_id_by_session_id.get(session_id)

        if 'created_at' not in user_info:
            return None
        if (user_info.get('created_at')
                + timedelta(seconds=self.session_duration) < datetime.now()):
            return None
        return user_info.get('user_id')
