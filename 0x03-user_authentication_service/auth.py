#!/usr/bin/env python3
"""
auth.py module file.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt and returns the salted hash as
    bytes
    """
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes


def _generate_uuid() -> str:
    """
    Implement a _generate_uuid function in the auth module. The function should
    return a string representation of a new UUID. Use the uuid module.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""
    def __init__(self):
        """
        Initialize an Auth.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and hashed password.
        If the user already exists, raises a ValueError.
        Returns the created User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        - Implement the Auth.valid_login method. It should expect email and
        password required arguments and return a boolean.
        - Try locating the user by email. If it exists, check the password with
        bcrypt.checkpw. If it matches return True. In any other case,
        return False.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        - Implement the Auth.create_session method. It takes an email string
        argument and returns the session ID as a string.
        - The method should find the user corresponding to the email, generate
        a new UUID and store it in the database as the user’s session_id,
        then return the session ID.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
