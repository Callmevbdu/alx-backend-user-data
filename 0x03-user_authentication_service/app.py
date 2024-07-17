#!/usr/bin/env python3
"""
Setting up a basic Flask app.
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    """
    A Flask app that has a single GET route ("/") and use flask.jsonify to
    return a JSON payload of the form: {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
