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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        - Implement the Auth.get_user_from_session_id method. It takes a single
        session_id string argument and returns the corresponding User or None.
        - If the session ID is None or no user is found, return None. Otherwise
        return the corresponding user.
        - Remember to only use public methods of self._db.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        - Implement Auth.destroy_session. The method takes a single user_id
        integer argument and returns None.
        - The method updates the corresponding user’s session ID to None.
        - Remember to only use public methods of self._db.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        - Implement the Auth.get_reset_password_token method. It take an email
        string argument and returns a string.
        - Find the user corresponding to the email. If the user does not exist,
        raise a ValueError exception. If it exists, generate a UUID and update
        the user’s reset_token database field. Return the token.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        - Implement the Auth.update_password method. It takes reset_token
        string argument and a password string argument and returns None.
        - Use the reset_token to find the corresponding user. If it does not
        exist, raise a ValueError exception.
        - Otherwise, hash the password and update the user’s hashed_password
        field with the new hashed password and the reset_token field to None.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
