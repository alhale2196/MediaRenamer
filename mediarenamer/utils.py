import os
import sys
import json
import re
from typing import Optional, List

try:
    from .exceptions import FileException
except ImportError:
    sys.path.append('./')
    from exceptions import MediaRenamerException, FileException, ParserException

try:
    from .file_utils import (
    write_to_file,
    get_current_directory_basename,
    get_list_of_folders_in_directory,
    get_list_of_files_in_directory,
    rename_file,
    rename_directory,
    get_file_extension,
    )
except ImportError:
    sys.path.append('./')
    from file_utils import (
        write_to_file,
        get_current_directory_basename,
        get_list_of_folders_in_directory,
        get_list_of_files_in_directory,
        rename_file,
        rename_directory,
        get_file_extension,
    )


def get_season_number_from_folder_name(folder_name: str) -> Optional[int]:
    """
    Gets the season number from a folder name.

    :param folder_name: The folder name.

    :return: The season number.
    """
    try:
        match = re.search(r'(?:Season\s*|S)(\d+)', folder_name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    except Exception as e:
        raise ParserException(str(e))

def get_episode_number_from_file_name(file_name: str) -> Optional[int]:
    """
    Gets the episode number from a file name.

    :param file_name: The file name.

    :return: The episode number.
    """
    try:
        match = re.search(r'(?:Episode\s*|E|Part\s*)(\d+)', file_name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    except Exception as e:
        raise ParserException(str(e))
