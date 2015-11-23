from __future__ import absolute_import, print_function, unicode_literals


class BaseCopyscapeError(Exception):
    pass


class CopyscapeKeyError(BaseCopyscapeError):
    pass


class CopyscapeUsernameError(BaseCopyscapeError):
    pass
