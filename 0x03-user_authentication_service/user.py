#!/usr/bin/env python3
"""
user.py file.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    A SQLAlchemy model named User for a database table named users:
    The model will have the following attributes:
        - id, the integer primary key
        - email, a non-nullable string
        - hashed_password, a non-nullable string
        - session_id, a nullable string
        - reset_token, a nullable string
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    hashed_password = db.Column(db.String(250), nullable=False)
    session_id = db.Column(db.String(250), nullable=True)
    reset_token = db.Column(db.String(250), nullable=True)
