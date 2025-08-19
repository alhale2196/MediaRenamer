from datetime import datetime
import sys
import re
from typing import Optional, List

try:
    from .exceptions import MediaRenamerException, ParserException
except ImportError:
    sys.path.append('./')
    from exceptions import MediaRenamerException, ParserException


def extract_season_number_from_directory_name(directory_name: str) -> Optional[str]:
    """
    Extracts the season number from a directory name.

    :param directory_name: The directory name.

    :return: The season number.
    """
    try:
        match = re.search(r'(?:Season\s*|S)(\d+)', directory_name, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        raise ParserException(str(e))


def extract_episode_number_from_file_name(file_name: str) -> Optional[str]:
    """
    Extracts the episode number from a file name.

    :param file_name: The file name.

    :return: The episode number.
    """
    try:
        match = re.search(r'(?:Episode\s*|E|Part\s*)(\d+)', file_name, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        raise ParserException(str(e))


def extract_show_year_from_directory_name(directory_name: str) -> Optional[str]:
    """
    Extracts the tv show year from a directory name.

    :param directory_name: The basename of the directory.

    :return: The tv show year.
    """
    try:
        pattern = re.compile(r"\((\d+)\)")
        numbers = pattern.findall(directory_name)
        if not numbers:
            return None
        if len(numbers) == 0:
            return None
        else:
            return numbers[0]

    except Exception as e:
        raise ParserException(str(e))


def extract_show_name_from_directory_basename(directory_basename:str) -> Optional[str]:
    """
    Extracts the show name from a directory basename.

    :param directory_basename:

    :return:
    """
    try:
        if not directory_basename:
            return None

        pattern = re.compile(r"\((\d+)\)")
        numbers = pattern.findall(directory_basename)
        if len(numbers) > 0:
            show_year = numbers[0]
        else:
            show_year = None

        if show_year:
            show_name = directory_basename.replace(show_year, '')
        else:
            show_name = directory_basename

        show_name = show_name.replace('(', '')
        show_name = show_name.replace(')', '')
        show_name = show_name.rstrip()
        return show_name

    except Exception as e:
        raise ParserException(str(e))


def extract_movie_year_from_string(movie_string: str) -> Optional[str]:
    """
    Extracts the movie year from a movie string.

    :param movie_string:
    :return:
    """
    try:
        match = re.search(r'\b(\d{4})\b', movie_string)
        if match:
            year = match.group(1)
            if int(year) < 1950 or int(year) > datetime.now().year:
                return None
            else:
                return year
        return None

    except Exception as e:
        raise ParserException(str(e))
