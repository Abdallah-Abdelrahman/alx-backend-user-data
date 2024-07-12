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
        if session_id:
            user_details = self.user_id_by_session_id.get(session_id)
            if user_details and "created_at" in user_details:
                if (
                    self.session_duration <= 0
                    or user_details["created_at"]
                    + timedelta(seconds=self.session_duration)
                    >= datetime.now()
                ):
                    return user_details.get("user_id")
        return None
