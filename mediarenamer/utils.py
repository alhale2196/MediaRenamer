import os
import sys
import json
from typing import Optional, List

try:
    from .exceptions import FileException
except ImportError:
    sys.path.append('./')
    from exceptions import FileException


def get_season_number_from_folder_name(folder_name: str) -> Optional[int]:
    """
    Gets the season number from a folder name.

    :param folder_name: The folder name.

    :return: The season number.
    """

def get_episode_number_from_file_name(file_name: str) -> Optional[int]:
    """
    Gets the episode number from a file name.

    :param file_name: The file name.

    :return: The episode number.
    """
