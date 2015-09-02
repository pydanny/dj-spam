class SpamNotFound(Exception):
    """When the system can't find spam the user defined"""


class B16DecodingFail(Exception):
    """When decoding from B16 fails"""
