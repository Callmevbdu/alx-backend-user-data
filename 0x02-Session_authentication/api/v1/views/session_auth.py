#!/usr/bin/env python3
"""
Flask view that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from typing import Tuple
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> Tuple[str, int]:
    """
    - use request.form.get() to retrieve email and password parameters
    - If email is missing or empty, return the JSON
    { "error": "email missing" } with the status code 400
    - If password is missing or empty, return the JSON
    { "error": "password missing" } with the status code 400
    - Retrieve the User instance based on the email - you must use the class
    method search of User (same as the one used for the BasicAuth)
        * If no User found, return the JSON { "error": "no user found for this
        email" } with the status code 404
        * If the password is not the one of the User found, return the JSON
        { "error": "wrong password" } with the status code 401 - you must use
        is_valid_password from the User instance
        * Otherwise, create a Session ID for the User ID:
            + You must use from api.v1.app import auth - WARNING: please import
            it only where you need it - not on top of the file (can generate
            circular import - and break first tasks of this project)
            + You must use auth.create_session(..) for creating a Session ID
            + Return the dictionary representation of the User - you must use
            to_json() method from User
            + You must set the cookie to the response - you must use the value
            of the environment variable SESSION_NAME as cookie name - tip
    """
    not_found_res = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404
    if len(users) <= 0:
        return jsonify(not_found_res), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return res
    return jsonify({"error": "wrong password"}), 401
