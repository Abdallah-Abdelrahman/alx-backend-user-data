#!/usr/bin/env python3
'''Module defines `BasicAuth` class'''
from typing import List, TypeVar
from flask import request
import base64

from api.v1.auth.auth import Auth


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
