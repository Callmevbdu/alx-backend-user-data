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
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return email, password
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:  # noqa
        """
        Retrieves the User instance based on email and password.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance for a given request.
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header:
            base64_value = self.extract_base64_authorization_header(auth_header)  # noqa
            decoded_value = self.decode_base64_authorization_header(base64_value)  # noqa
            email, password = self.extract_user_credentials(decoded_value)
            if email and password:
                return self.user_object_from_credentials(email, password)
        return None
