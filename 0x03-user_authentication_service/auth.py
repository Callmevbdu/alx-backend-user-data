#!/usr/bin/env python3
"""
auth.py module file.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt and returns the salted hash as bytes
    """
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes
