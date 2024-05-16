#!/usr/bin/env python3
""" filtered logger module
"""
import re


patterns = {
    "extract": lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    "replace": lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: list[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """ Return the log message obfuscated
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)
