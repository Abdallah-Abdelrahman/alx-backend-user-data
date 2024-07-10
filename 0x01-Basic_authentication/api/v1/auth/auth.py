#!/usr/bin/env python3
'''Module defines `Auth` class'''
from typing import List, TypeVar
from flask import request
import re


class Auth:
    '''class definition'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False'''
        if not path or not excluded_paths:
            return True
        if path[-1] == '/':
            path = path[:-1]
        is_excluded = path in [p[:-1] if p[-1] == '/'
                               else p for p in excluded_paths]
        for ex in excluded_paths:
            pattern = ex.split('/')[-1]

            if re.search(rf'{pattern}', path):
                # to check agains trailing astrisk (*)
                # ex: excluded_paths = ["/api/v1/stat*"]
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
