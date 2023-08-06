# -*- coding: utf-8 -*-

__all__ = ("NotAFileError", "DirectoryNotFoundError")


class NotAFileError(OSError):
    pass


class DirectoryNotFoundError(FileNotFoundError):
    pass
