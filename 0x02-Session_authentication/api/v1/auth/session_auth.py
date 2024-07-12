#!/usr/bin/env python3
"""
Session Authentication
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    A class SessionAuth that inherits from Auth.
    """
    def __init__(self):
        """
        init function
        """
        super().__init__()
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
