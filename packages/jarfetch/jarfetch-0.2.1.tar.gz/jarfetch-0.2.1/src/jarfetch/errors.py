class ServerJarsAPIError(Exception):
    """Exception occurred while attempting to fetch from an endpoint"""


class MD5HashMismatch(Exception):
    """Calculated MD5 hash for file does not match provided details"""
