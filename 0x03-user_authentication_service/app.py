#!/usr/bin/env python3
"""
Setting up a basic Flask app.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def hello():
    """
    A Flask app that has a single GET route ("/") and use flask.jsonify to
    return a JSON payload of the form: {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    - Implement the end-point to register a user. Define a users function that
    implements the POST /users route.
    - Import the Auth object and instantiate it at the root of the module.
    - The end-point should expect two form data fields: "email" and "password".
    If the user does not exist, return:
    {"email": "<registered email>", "message": "user created"}
    - If the user is already registered, catch the exception and return a JSON
    payload of the form {"message": "email already registered"} and return a
    400 status code.
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)

        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    - Implement a login function to respond to the POST /sessions route.
    - The request is expected to contain form data with "email" and a
    "password" fields.
    - If the login information is incorrect, use flask.abort to respond with a
    401 HTTP status.
    - Otherwise, create a new session for the user, store it the session ID as
    a cookie with key "session_id" on the response and return a JSON payload of
    the form: {"email": "<user email>", "message": "logged in"}.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    - Implement a logout function to respond to the DELETE /sessions route.
    - The request is expected to contain the session ID as a cookie with key
    "session_id".
    - Find the user with the requested session ID. If the user exists destroy
    the session and redirect the user to GET /. If the user does not exist,
    respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """
    - Implement a profile function to respond to the GET /profile route.
    - The request is expected to contain a session_id cookie. Use it to find
    the user. If the user exist, respond with a 200 HTTP status and the
    following JSON payload: {"email": "<user email>"}
    - If the session ID is invalid or the user does not exist, respond with a
    403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
