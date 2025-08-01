import os
import sys
import json
from typing import List, Optional

try:
    from .exceptions import FileException
except ImportError:
    sys.path.append('./')
    from exceptions import FileException


def write_to_file(filename: str, content: str, overwrite: bool = False, json_data: bool = True) -> bool:
    """
    Writes or appends content to a file.

    :param filename: The filename to write.
    :param content: The content to write.
    :param overwrite: Overwrite existing content.
    :param json_data: Is the content JSON data.

    :return: True if the file was written, False otherwise.
    """
    if overwrite == True:
        if json_data == True:
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
        if json_data == True:
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
    return False

def get_current_directory_basename() -> Optional[str]:
    """
    Gets the current directory name.

    :return: Current directory name.
    """
    try:
        current_directory_path = os.getcwd()
        current_directory_basename = os.path.basename(current_directory_path)
        return current_directory_basename
    except Exception as e:
        raise FileException(str(e))

def get_list_of_folders_in_directory(directory: str) -> Optional[List[str]]:
    """
    Gets a list of all folders in a directory.

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

def get_list_of_files_in_directory(directory: str) -> Optional[List[str]]:
    """
    Gets a list of all files in a directory.

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

def get_file_extension(filename: str) -> Optional[str]:
    """
    Gets the file extension.

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
