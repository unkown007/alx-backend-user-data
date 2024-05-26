#!/usr/bin/env python3
""" Module to manage API authentication
"""
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """ Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check whether a path/resource requires authentication
        Args:
            path(str): endpoint path
            excluded_paths(List[str]): list of excluded path for auth
        Return:
            - True if path no in excluded_paths else False
        Raises:
            Nothing expected
        """
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
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
        """ Look for Authorization header in the request
        Args:
            request: Flask request
        Return:
            - None
        Raises:
            Nothing expected
        """
        if request is None or request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user requesting a resource
        Args:
            request: Flask request
        Return:
            - None
        Raises:
            Nothing
        """
        return None

    def session_cookie(self, request=None):
        """ Return a cookie value from a request
        """
        if request is None:
            return None
        SESSION_NAME = os.getenv('SESSION_NAME')

        if SESSION_NAME is None:
            return None

        session_id = request.cookies.get(SESSION_NAME)

        return session_id
