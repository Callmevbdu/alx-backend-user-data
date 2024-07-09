#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # noqa
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.
        """
        if authorization_header is None or not isinstance(authorization_header, str):  # noqa
            return None
        if authorization_header.startswith("Basic "):
            return authorization_header.split(" ", 1)[1]
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # noqa
        """
        Decodes the Base64-encoded authorization header.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):  # noqa
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # noqa
        """
        Extracts the user email and password from the Base64-decoded
        authorization header.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):  # noqa
            return None, None
        if ':' in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return email, password
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        """
        Retrieves the User instance based on email and password.
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
