# -*- coding: utf-8 -*-

__all__ = (
    # exceptions
    "DirectoryNotFoundError",
    "NotAFileError",
    # types
    "StrPath",
    "StrPaths",
    # path
    # - stringify
    "stringify_path",
    "stringify_paths",
    # - single existence
    "check_if_path_exists",
    "check_if_file_exists",
    "check_if_dir_exists",
    # - multiple existences
    "check_if_paths_exist",
    "check_if_files_exist",
    "check_if_dirs_exist",
    # - child path(s) search
    "get_paths",
    "get_files",
    "get_dirs",
    # - empty directory check
    "is_empty_dir",
    "is_empty_dir_unsafe",
    "are_empty_dirs",
    "are_empty_dirs_unsafe",
)

from kaparoo.filesystem.exceptions import DirectoryNotFoundError, NotAFileError
from kaparoo.filesystem.path import (
    are_empty_dirs,
    are_empty_dirs_unsafe,
    check_if_dir_exists,
    check_if_dirs_exist,
    check_if_file_exists,
    check_if_files_exist,
    check_if_path_exists,
    check_if_paths_exist,
    get_dirs,
    get_files,
    get_paths,
    is_empty_dir,
    is_empty_dir_unsafe,
    stringify_path,
    stringify_paths,
)
from kaparoo.filesystem.types import StrPath, StrPaths
