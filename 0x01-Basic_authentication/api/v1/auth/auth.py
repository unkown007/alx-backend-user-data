#!/usr/bin/env python3
""" Module to manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check whether a path/resource requires authentication
        Args:
            path(str): endpoint path
            excluded_paths(List[str]): list of excluded path for auth
        Return:
            - False
        Raises:
            Nothing expected
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Look for Authorization header in the request
        Args:
            request: Flask request
        Return:
            - None
        Raises:
            Nothing expected
        """
        return None

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
