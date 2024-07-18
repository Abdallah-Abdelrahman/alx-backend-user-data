#!/usr/bin/env python3
'''
Main file
'''
import requests

API = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    '''Add new user by `email` and `password`'''
    data = {'email': email, 'password': password}
    resp = requests.post(API+'/users', data=data)
    assert resp.status_code == 200
    assert resp.json().get('message') == 'user created'


def log_in_wrong_password(email: str, password: str) -> None:
    '''Log-in with wrong credentials'''
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(API+'/sessions', data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Log-in with correct credentials'''
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(API+'/sessions', data=data)
    assert resp.status_code == 200
    assert resp.json().get('message') == 'logged in'


def profile_unlogged() -> None:
    '''Access profile w/out log-in'''
    resp = requests.get(API+'/profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Access profile w/ correct `session_id`'''
    resp = requests.get(API+'/profile', cookies={'session_id': session_id})
    assert resp.status_code == 200
    assert resp.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    '''Log-out and destory the session'''
    resp = requests.delete(API+'/sessions', cookies={'session_id': session_id})
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    '''Request another token'''
    resp = requests.post(API+'/reset_password', data={'email': email})
    assert resp.status_code == 200
    assert 'reset_token' in resp.json()
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Updates user's password'''
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    resp = requests.put(API+'reset_password', data=data)
    assert resp.status_code == 200
    assert resp.json().get('message') == 'Password updated'


EMAIL = 'guillaume@holberton.io'
PASSWD = 'b4l0u'
NEW_PASSWD = 't4rt1fl3tt3'
if __name__ == '__main__':

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
