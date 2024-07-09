#!/usr/bin/env python3
'''Module defines `Auth` class'''
from typing import List, TypeVar
from flask import request


class Auth:
    '''class definition'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False'''
        return False

    def authorization_header(self, request=None) -> str:
        '''that returns None'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''that returns None'''
        return None
