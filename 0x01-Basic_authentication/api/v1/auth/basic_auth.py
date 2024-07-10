#!/usr/bin/env python3
'''Module defines `BasicAuth` class'''
from typing import List, TypeVar
from flask import request

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''class definition'''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''returns the Base64.
        part of the Authorization header for a Basic Authentication
        '''
        ah = authorization_header
        if not ah or not isinstance(ah, str) or ah.startswith('Basic '):
            return None
        return ah.split()[-1]
