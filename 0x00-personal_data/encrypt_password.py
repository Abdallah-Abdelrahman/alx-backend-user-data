#!/usr/bin/env python3
'''Module defines `hash_password` function'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''Hashes a password using bcrypt and returns the salted, hashed password.
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
