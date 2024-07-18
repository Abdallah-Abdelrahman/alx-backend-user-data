#!/usr/bin/env python3
'''
Main file
'''
import requests


def register_user(email: str, password: str) -> None:
    '''Add new user by `email` and `password`'''


def log_in_wrong_password(email: str, password: str) -> None:
    '''Log-in with wrong credentials'''


def log_in(email: str, password: str) -> str:
    '''Log-in with correct credentials'''


def profile_unlogged() -> None:
    '''Access profile w/out log-in'''


def profile_logged(session_id: str) -> None:
    '''Access profile w/ correct `session_id`'''


def log_out(session_id: str) -> None:
    '''Log-out and destory the session'''


def reset_password_token(email: str) -> str:
    '''Request another token'''


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Updates user's password'''


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
