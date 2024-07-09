#!/usr/bin/env python3
"""
Auth.py file.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    A class to manage the API authentication.
    - import request from flask
    - class name Auth
    - public method
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
    that returns False - path and excluded_paths will be used later, now, you
    don’t need to take care of them
    - public method def authorization_header(self, request=None) -> str: that
    returns None - request will be the Flask request object
    - public method def current_user(self, request=None) -> TypeVar('User'):
    that returns None - request will be the Flask request object
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Placeholder method for checking if authentication is required.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Placeholder method for extracting the authorization header.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for retrieving the current authenticated user.
        """
        return None
