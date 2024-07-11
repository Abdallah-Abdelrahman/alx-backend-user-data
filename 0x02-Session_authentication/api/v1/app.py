#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv('AUTH_TYPE'):
    from api.v1.auth.auth import Auth
    from api.v1.auth.basic_auth import BasicAuth
    from api.v1.auth.session_auth import SessionAuth

    AUTH = getenv('AUTH_TYPE')

    if AUTH == 'session_auth':
        auth = SessionAuth()
    elif AUTH == 'basic_auth':
        auth = BasicAuth()
    else:
        auth = Auth()


@app.before_request
def before_request_():
    '''run before each request to check for user and header'''
    if not auth:
        return
    excluded = ['/api/v1/status/', '/api/v1/unauthorized/',
                '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded):
        return
    if not auth.authorization_header(request):
        abort(401)
    request.current_user = auth.current_user(request)
    if not auth.current_user(request):
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Not authorized access
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Not allowed access
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
