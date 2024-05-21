#!/usr/bin/env python3
""" Module to manage API authentication
"""
from flask import request
from typing import List, TypeVar
import re


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
        for pth in excluded_paths:
            if re.search(f"^{path}", pth) is not None:
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
