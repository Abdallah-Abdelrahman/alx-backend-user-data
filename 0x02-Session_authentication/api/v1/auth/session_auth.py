#!/usr/bin/env python3
'''Module defines `SessionAuth` class'''
from typing import List, TypeVar
from flask import request
import base64

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''class definition'''
    pass
