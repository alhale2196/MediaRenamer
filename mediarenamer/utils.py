import os
import sys
import json
import re
import logging
from typing import Optional, List

try:
    from .exceptions import MediaRenamerException, ParserException

except ImportError:
    sys.path.append('./')
    from exceptions import MediaRenamerException, ParserException


def extract_season_number_from_directory_name(directory_name: str, log: logging.Logger) -> Optional[int]:
    """
    Extracts the season number from a directory name.

    :param directory_name: The directory name.
    :param log: The configured logger to write to.

    :return: The season number.
    """
    log.debug(f'Getting season number from directory {directory_name}')
    try:
        match = re.search(r'(?:Season\s*|S)(\d+)', directory_name, re.IGNORECASE)
        if match:
            log.debug(f'Found season number for directory name: {directory_name}. Season number: {match.group(1)}')
            return int(match.group(1))
        log.debug(f'Could not find season number for directory name: {directory_name}')
        return None
    except Exception as e:
        log.exception(str(e))
        raise ParserException(str(e))

def extract_episode_number_from_file_name(file_name: str, log: logging.Logger) -> Optional[int]:
    """
    Extracts the episode number from a file name.

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

def extract_show_year_from_directory_name(directory_name: str, log: logging.Logger) -> Optional[int]:
    """
    Extracts the tv show year from a directory name.

    :param directory_name: The basename of the directory.
    :param log: The configured logger to write to.

    :return: The tv show year.
    """
    log.debug(f'Extracting tv show year from directory name: {directory_name}')
    try:
        pattern = re.compile(r"\((\d+)\)")
        numbers = pattern.findall(directory_name)
        if not numbers:
            log.error(f'Could not extract tv show year from directory name: {directory_name}')
            return None
        if len(numbers) == 0:
            log.error(f'Could not extract tv show year from directory name: {directory_name}')
        else:
            log.debug(f'Extracted tv show year: {numbers} from directory name: {directory_name}')
            return int(numbers[0])

    except Exception as e:
        log.exception(str(e))
        raise ParserException(str(e))
