#!/usr/bin/env python3
'''Module defines `_hash_password` function'''
from flask import Flask, jsonify, request, abort, make_response
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
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            resp = make_response({
                'email': email,
                'message': 'logged in'
            })
            resp.set_cookie('session_id', session_id)
            return resp
    except ValueError:
        abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
