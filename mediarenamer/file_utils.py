import os
import sys
import json
from typing import List, Optional

try:
    from .config import ALLOWED_FILE_EXTENSIONS
    from .exceptions import MediaRenamerException, FileException
    from .utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name
except ImportError:
    sys.path.append('./')
    from config import ALLOWED_FILE_EXTENSIONS
    from exceptions import MediaRenamerException, FileException, ParserException
    from utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name


def write_to_file(filename: str, content: str, overwrite: bool = False, json_data: bool = True) -> bool:
    """
    Writes or appends content to a file.

    :param filename: The filename to write.
    :param content: The content to write.
    :param overwrite: Overwrite existing content.
    :param json_data: Is the content JSON data.

    :return: True if the file was written, False otherwise.
    """
    if overwrite:
        if json_data:
            try:
                with open(filename, 'w') as f:
                    json.dump(content, f, indent=4)
                    return True
            except Exception as e:
                raise FileException(str(e))
        else:
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                    return True
            except Exception as e:
                raise FileException(str(e))
    else:
        if json_data:
            try:
                with open(filename, 'a') as f:
                    json.dump(content, f, indent=4)
                    return True
            except Exception as e:
                raise FileException(str(e))
        else:
            try:
                with open(filename, 'a') as f:
                    f.write(content)
                    return True
            except Exception as e:
                raise FileException(str(e))


def extract_current_directory_basename() -> Optional[str]:
    """
    Extracts the current directory name.

    :return: Current directory name.
    """
    try:
        current_directory_path = os.getcwd()
        current_directory_basename = os.path.basename(current_directory_path)
        return current_directory_basename
    except Exception as e:
        raise FileException(str(e))


def extract_list_of_folders_in_directory(directory: str) -> Optional[List[str]]:
    """
    Extracts a list of all folders in a directory.

    :param directory: The directory to get folders from.

    :return: List of all folders in the directory.
    """
    folders = []
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                folders.append(full_path)
        return folders
    except Exception as e:
        raise FileException(str(e))


def extract_list_of_files_in_directory(directory: str) -> Optional[List[str]]:
    """
    Extracts a list of all files in a directory.

    :param directory: The directory to get files from.

    :return: List of all files in the directory.
    """
    files = []
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
        return files
    except Exception as e:
        raise FileException(str(e))


def rename_file(current_file_name: str, new_file_name: str) -> bool:
    """
    Renames a file.

    :param current_file_name: The current file name.
    :param new_file_name: The new file name.

    :return: True if the file was renamed, False otherwise.
    """
    try:
        os.rename(current_file_name, new_file_name)
        return True
    except Exception as e:
        raise FileException(str(e))


def rename_directory(current_directory_name: str, new_directory_name: str) -> bool:
    """
    Renames a directory.

    :param current_directory_name: The current directory name.
    :param new_directory_name: The new directory name.

    :return: True if the directory was renamed, False otherwise.
    """
    try:
        os.rename(current_directory_name, new_directory_name)
        return True
    except Exception as e:
        raise FileException(str(e))


def extract_file_extension(filename: str) -> Optional[str]:
    """
    Extracts the file extension.

    :param filename: The filename.

    :return: File extension.
    """
    try:
        extension = filename.split('.')[-1]
        if extension:
            return extension
        else:
            return None
    except Exception as e:
        raise FileException(str(e))


def delete_file(file_name: str) -> bool:
    """

    :param file_name:

    :return:
    """
    try:
        os.remove(file_name)
        return True
    except Exception as e:
        raise FileException(str(e))


def parse_files_in_directory_to_delete(files_in_directory: List[str]) -> Optional[List[str]]:
    """

    :param files_in_directory:

    :return:
    """
    files_to_delete = []
    try:
        for file_in_directory in files_in_directory:
            file_extension = extract_file_extension(file_in_directory)
            if file_extension not in ALLOWED_FILE_EXTENSIONS:
                files_to_delete.append(file_in_directory)
        return files_to_delete
    except Exception as e:
        raise ParserException(str(e))


def scan_directory(directory: str) -> dict:
    """

    :param directory:
    :return:
    """
    scan_results = {}
    season_folders = []
    episode_files = []
    unknown_folders = []
    unknown_files = []
    files_to_delete = []

    directory_basename = extract_directory_basename(directory)
    folders_in_directory = extract_list_of_folders_in_directory(directory)
    files_in_directory = extract_list_of_files_in_directory(directory)

    if folders_in_directory:
        for folder_in_directory in folders_in_directory:
            season_number = extract_season_number_from_directory_name(folder_in_directory)
            if season_number:
                 season_folders.append(folder_in_directory)
            else:
                unknown_folders.append(folder_in_directory)

    if files_in_directory:
        files_in_directory_to_delete = parse_files_in_directory_to_delete(files_in_directory)
        if files_in_directory_to_delete:
            files_to_delete.extend(files_in_directory_to_delete)

        for file_in_directory in files_in_directory:
            if file_in_directory in files_to_delete:
                continue
            episode_number = extract_episode_number_from_file_name(file_in_directory)
            if episode_number:
                episode_files.append(file_in_directory)
            else:
                unknown_files.append(file_in_directory)

    master_season_number = extract_season_number_from_directory_name(directory_basename)
    if master_season_number:
        if len(master_season_number) == 1:
            master_season_number = '0' + master_season_number
    else:
        master_season_number = None

    scan_results['directory_basename'] = directory_basename
    scan_results['season_number'] = master_season_number
    scan_results['season_folders'] = season_folders
    scan_results['episode_files'] = episode_files
    scan_results['unknown_folders'] = unknown_folders
    scan_results['unknown_files'] = unknown_files
    scan_results['files_to_delete'] = files_to_delete
    return scan_results


def extract_directory_basename(directory: str) -> Optional[str]:
    """

    :param directory:
    :return:
    """
    try:
        basename = os.path.basename(directory)
        if basename:
            return basename
        else:
            return None

    except Exception as e:
        raise FileException(str(e))


def extract_file_basename(file_name: str) -> Optional[str]:
    """

    :param file_name:
    :return:
    """
    try:
        basename = os.path.basename(file_name)
        if basename:
            return basename
        else:
            return None

    except Exception as e:
        raise FileException(str(e))


def create_directory_for_movie_file(file_name: str) -> Optional[str]:
    """
    Creates a directory for a movie file and moves file to directory.

    :param file_name: Name of the movie file.

    :return: Path to the new directory.
    """
    try:
        file_basename = os.path.basename(file_name)
        if not file_basename:
            return

        actual_file_name = file_basename.split('.')[0]
        if not actual_file_name:
            return

        current_directory = os.getcwd()
        new_directory = os.path.join(current_directory, actual_file_name)
        if os.path.exists(new_directory):
            return
        os.mkdir(new_directory)
        return new_directory

    except Exception as e:
        raise FileException(str(e))


















