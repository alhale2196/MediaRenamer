import os
import sys
import json
import re
import logging
from typing import Optional, List

try:
    from .exceptions import MediaRenamerException, ParserException
    from .file_utils import write_to_file, get_current_directory_basename, get_list_of_folders_in_directory, \
        get_list_of_files_in_directory, rename_file, rename_directory, get_file_extension

except ImportError:
    sys.path.append('./')
    from exceptions import MediaRenamerException, ParserException
    from file_utils import write_to_file, get_current_directory_basename, get_list_of_folders_in_directory, \
        get_list_of_files_in_directory, rename_file, rename_directory, get_file_extension


def get_season_number_from_folder_name(folder_name: str, log: logging.Logger) -> Optional[int]:
    """
    Gets the season number from a folder name.

    :param folder_name: The folder name.
    :param log: The configured logger to write to.

    :return: The season number.
    """
    log.debug(f'Getting season number from {folder_name}')
    try:
        match = re.search(r'(?:Season\s*|S)(\d+)', folder_name, re.IGNORECASE)
        if match:
            log.debug(f'Found season number for folder name: {folder_name}. Season number: {match.group(1)}')
            return int(match.group(1))
        log.debug(f'Could not find season number for folder name: {folder_name}')
        return None
    except Exception as e:
        log.exception(str(e))
        raise ParserException(str(e))

def get_episode_number_from_file_name(file_name: str, log: logging.Logger) -> Optional[int]:
    """
    Gets the episode number from a file name.

    :param file_name: The file name.
    :param log: The configured logger to write to.

    :return: The episode number.
    """
    log.debug(f'Getting episode number from file name: {file_name}')
    try:
        match = re.search(r'(?:Episode\s*|E|Part\s*)(\d+)', file_name, re.IGNORECASE)
        if match:
            log.debug(f'Found episode number for file name: {file_name}. Episode number: {match.group(1)}')
            return int(match.group(1))
        log.debug(f'Could not find episode number for file name: {file_name}')
        return None
    except Exception as e:
        log.exception(str(e))
        raise ParserException(str(e))
