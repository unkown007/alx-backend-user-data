#!/usr/bin/env python3
""" Module to implement Session Authentication with expiration time
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiration time Authentication class
    """

    def __init__(self):
        """ Initliaze the class
        """
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """ Creates a session with expiration time
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get a user based on a session_id
        """
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        if session_dictionary.get("created_at") is None:
            return None

        created_at = session_dictionary.get("created_at")
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None

        return session_dictionary.get("user_id")
