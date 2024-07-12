#!/usr/bin/env python3
"""
Actually you have 2 authentication systems:
    * Basic authentication
    * Session authentication
Now you will add an expiration date to a Session ID.
"""
import os
from flask import request
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    A class SessionExpAuth that inherits from SessionAuth.
    """
    def __init__(self) -> None:
        """
        Assign an instance attribute session_duration:
            - To the environment variable SESSION_DURATION casts to an
            integer
            - If this environment variable doesn’t exist or can’t be
            parse to an integer, assign to 0
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        - Create a Session ID by calling super() - super() will call the
        create_session() method of SessionAuth
        - Return None if super() can’t create a Session ID
        - Use this Session ID as key of the dictionary user_id_by_session_id -
        the value for this key must be a dictionary
        (called “session dictionary”):
            * The key user_id must be set to the variable user_id
            * The key created_at must be set to the current datetime - you must
            use datetime.now()
        - Return the Session ID created
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        - Return None if session_id is None
        - Return None if user_id_by_session_id doesn’t contain any key equals
        to session_id
        - Return the user_id key from the session dictionary if
        self.session_duration is equal or under 0
        - Return None if session dictionary doesn’t contain a key created_at
        - Return None if the created_at + session_duration seconds are before
        the current datetime. datetime - timedelta
        - Otherwise, return user_id from the session dictionary
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
