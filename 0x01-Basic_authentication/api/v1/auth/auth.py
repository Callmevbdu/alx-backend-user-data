#!/usr/bin/env python3
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
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        # Placeholder implementation (returns False)
        return False

    def authorization_header(self, request=None) -> str:
        # Placeholder implementation (returns None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        # Placeholder implementation (returns None)
        return None
