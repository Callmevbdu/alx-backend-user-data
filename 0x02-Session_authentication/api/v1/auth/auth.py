#!/usr/bin/env python3
"""
Auth.py file.
"""
import re
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
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Placeholder method for extracting the authorization header.
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for retrieving the current authenticated user.
        """
        return None
