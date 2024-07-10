#!/usr/bin/env python3
'''Module defines `BasicAuth` class'''
from typing import List, TypeVar
from flask import request
import base64

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    '''class definition'''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''returns the Base64.
        part of the Authorization header for a Basic Authentication
        '''
        ah = authorization_header
        if not ah or not isinstance(ah, str) or not ah.startswith('Basic '):
            return None
        return ah.split()[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        ''' returns the decoded value.
        of a Base64 string base64_authorization_header
        '''
        b64 = base64_authorization_header
        if not b64 or not isinstance(b64, str):
            return None
        try:
            bytes_ = b64.encode('utf8')
            bytes64 = base64.b64decode(bytes_)
            return bytes64.decode('utf8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''returns the user email and password from the Base64 decoded value'''
        decoded_ah = decoded_base64_authorization_header
        if not decoded_ah\
                or not isinstance(decoded_ah, str) or ':' not in decoded_ah:
            return (None, None)
        return tuple(decoded_ah.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''returns the User instance based on his email and password'''
        if isinstance(user_email, str) and isinstance(user_email, str):
            try:
                found_email = User.search({'email': user_email})
            except Exception:
                return None
            # print(found_email)
            if len(found_email) <= 0:
                return None
            if found_email[0].is_valid_password(user_pwd):
                return found_email[0]
        return None
