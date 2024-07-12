#!/usr/bin/env python3
"""
Flask view that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from typing import Tuple
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    - use request.form.get() to retrieve email and password parameters
    - If email is missing or empty, return the JSON
    { "error": "email missing" } with the status code 400
    - If password is missing or empty, return the JSON
    { "error": "password missing" } with the status code 400
    - Retrieve the User instance based on the email - you must use the class
    method search of User (same as the one used for the BasicAuth)
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID
    session_id = auth.create_session(user.id)

    # Return user info and set cookie
    response_data = user.to_json()
    response = jsonify(response_data)
    response.set_cookie(app.config['SESSION_NAME'], session_id)

    return response
