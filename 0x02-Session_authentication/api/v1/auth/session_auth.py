#!/usr/bin/env python3
""" Module to implement session authentication mecanism
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Authentication implementation class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        Args:
            user_id(str): User ID
        Returns:
            Session id
        """
        if not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get a user_id bassed on session_id
        Args:
            session_id(str): User Session ID
        Returns:
            user id
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
