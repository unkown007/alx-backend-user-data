#!/usr/bin/env python3
""" Module to implement Basic API authentication
"""
from api.v1.auth.auth import Auth
import re


class BasicAuth(Auth):
    """ Basic Authentication class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """ Get Authorization header and extract it
        Args:
            authorization_header(str): Base64 encoded string
        Return:
            Base64 part of the Authorization header for a Basic Authentication
        """
        if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                re.search('^Basic ', authorization_header.strip()) is None:
            return None
        return authorization_header.strip().split(' ')[1]
