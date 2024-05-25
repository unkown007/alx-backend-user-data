#!/usr/bin/env python3
""" Module to implement Basic API authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import re
import base64


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """ Decode an Base64 string in Authorization header
        Args:
            base64_authorization_header(str): base64 enconded string
        Return
            decoded string
        Raise:
            binascii.Error
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            b64_decoded = base64.b64decode(base64_authorization_header)
            return b64_decoded.decode("utf-8")
        except base64.binascii.Error as error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Get user credentials
        Args:
            decoded_base64_authorization_header: user credentials
        Return:
            tuple containing user credentials
        Raises:
            Nothing
        """
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                re.search(":", decoded_base64_authorization_header) is None:
            return (None, None)

        return tuple(re.split(":", decoded_base64_authorization_header))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """ Authenticate a user
        Args:
            user_email(str): user email
            user_pwd(pwd): user password
        Return:
            User object
        Raises
            Nothing
        """
        if user_email is None or\
                not isinstance(user_email, str) or\
                user_pwd is None or\
                not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
