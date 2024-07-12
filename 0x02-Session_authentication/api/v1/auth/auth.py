#!/usr/bin/env python3
'''Module defines `Auth` class'''
from typing import List, TypeVar
from os import getenv
import re


class Auth:
    '''class definition'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False'''
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        if path[-1] == '/':
            path = path[:-1]

        is_excluded = path in [p[:-1] if p[-1] == '/'
                               else p for p in excluded_paths
                               if isinstance(p, str)]
        for pattern in excluded_paths:
            if '*' not in pattern:
                continue
            pattern = pattern.replace("*", ".*")  # Convert wildcard to regex
            if re.match(pattern, path):
                return False

        return not is_excluded

    def authorization_header(self, request=None) -> str:
        '''that returns None'''
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''that returns None'''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if not request:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
