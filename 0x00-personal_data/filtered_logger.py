#!/usr/bin/env python3
"""
a function called filter_datum that returns the log message obfuscated:
* Arguments:
    - fields: a list of strings representing all fields to obfuscate
    - redaction: a string representing by what the field will be obfuscated
    - message: a string representing the log line
    - separator: a string representing by which character is separating all
    fields in the log line (message)
* The function should use a regex to replace occurrences of certain field
values.
* filter_datum should be less than 5 lines long and use re.sub to perform the
substitution with a single regex.
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list[str]): List of fields to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): Log line containing fields.
        separator (str): Character separating fields in the log line.

    Returns:
        str: Obfuscated log message.
    """
    pattern = f"({'|'.join(re.escape(field) for field in fields)})"
    return re.sub(pattern, redaction, message, flags=re.IGNORECASE)
