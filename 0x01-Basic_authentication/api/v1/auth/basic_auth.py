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
            b64_decoded = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            return b64_decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
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
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        pattern = r'(?P<user>[^:]+):(?P<password>.+)'
        field_match = re.fullmatch(
            pattern,
            decoded_base64_authorization_header.strip()
        )
        if field_match is not None:
            user = field_match.group("user")
            password = field_match.group("password")
            return user, password
        return (None, None)

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
        if not isinstance(user_email, str) or\
                not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve the current user for the request
        Args:
            request: user request
        Return:
            User object
        Raise:
            nothing
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        user = self.user_object_from_credentials(
                email,
                password)
        return user
