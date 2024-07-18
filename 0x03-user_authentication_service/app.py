#!/usr/bin/env python3
'''Module defines `_hash_password` function'''
from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    '''main route'''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'])
def users():
    '''Register new user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email, 'message': 'user created'}), 200
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'])
def login():
    '''Register new user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        # if this fails it will raise NoResultFound
        AUTH.valid_login(email, password)
    except NoResultFound:
        abort(401)

    session_id = AUTH.create_session(email)
    resp = make_response({
        'email': email,
        'message': 'logged in'
    })
    resp.set_cookie('session_id', session_id)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
