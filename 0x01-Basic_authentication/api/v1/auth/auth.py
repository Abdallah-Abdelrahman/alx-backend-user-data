#!/usr/bin/env python3
'''Module defines `Auth` class'''
from typing import List, TypeVar
from flask import request


class Auth:
    '''class definition'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False'''
        if not path or not excluded_paths:
            return True
        if path[-1] == '/':
            path = path[:-1]
        is_excluded = path in [p[:-1] if p[-1] == '/'\
                else p for p in excluded_paths]

        return not is_excluded

    def authorization_header(self, request=None) -> str:
        '''that returns None'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''that returns None'''
        return None
