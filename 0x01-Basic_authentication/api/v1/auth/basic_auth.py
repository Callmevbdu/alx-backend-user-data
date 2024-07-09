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
