#!/usr/bin/env python3
""" Module defines encriptions functions to password """
import bcrypt


def hash_password(pwd: str) -> bytes:
    """ Return a salted, hashed password """
    pwd_bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if wether a password is valid """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
