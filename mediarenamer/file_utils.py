import os
import sys
import json
import logging
from typing import List, Optional

try:
    from .exceptions import MediaRenamerException, FileException
except ImportError:
    sys.path.append('./')
    from exceptions import MediaRenamerException, FileException


def write_to_file(filename: str, content: str, log: logging.Logger, overwrite: bool = False, json_data: bool = True) -> bool:
    """
    Writes or appends content to a file.

    :param filename: The filename to write.
    :param content: The content to write.
    :param log: The configured logger to write to.
    :param overwrite: Overwrite existing content.
    :param json_data: Is the content JSON data.

    :return: True if the file was written, False otherwise.
    """
    if overwrite:
        if json_data:
            try:
                log.debug(f'Writing JSON data to file: {filename}')
                with open(filename, 'w') as f:
                    json.dump(content, f, indent=4)
                    return True
            except Exception as e:
                log.exception(str(e))
                raise FileException(str(e))
        else:
            try:
                log.debug(f'Writing data to file: {filename}')
                with open(filename, 'w') as f:
                    f.write(content)
                    return True
            except Exception as e:
                log.exception(str(e))
                raise FileException(str(e))
    else:
        if json_data:
            try:
                log.debug(f'Appending JSON data to file: {filename}')
                with open(filename, 'a') as f:
                    json.dump(content, f, indent=4)
                    return True
            except Exception as e:
                log.exception(str(e))
                raise FileException(str(e))
        else:
            try:
                log.debug(f'Appending data to file: {filename}')
                with open(filename, 'a') as f:
                    f.write(content)
                    return True
            except Exception as e:
                log.exception(str(e))
                raise FileException(str(e))

def extract_current_directory_basename(log: logging.Logger) -> Optional[str]:
    """
    Extracts the current directory name.

    :param log: The configured logger to write to.

    :return: Current directory name.
    """
    log.debug(f'Getting basename of the current directory')
    try:
        current_directory_path = os.getcwd()
        log.debug(f'Current directory: {current_directory_path}')
        current_directory_basename = os.path.basename(current_directory_path)
        log.debug(f'Current directory basename: {current_directory_basename}')
        return current_directory_basename
    except Exception as e:
        log.exception(str(e))
        raise FileException(str(e))

def extract_list_of_folders_in_directory(directory: str, log: logging.Logger) -> Optional[List[str]]:
    """
    Extracts a list of all folders in a directory.

    :param directory: The directory to get folders from.
    :param log: The configured logger to write to.

    :return: List of all folders in the directory.
    """
    log.debug(f'Getting list of all folders in directory: {directory}')
    folders = []
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                folders.append(full_path)
        log.debug(f'Found {len(folders)} folders in directory: {directory}')
        return folders
    except Exception as e:
        log.exception(str(e))
        raise FileException(str(e))

def extract_list_of_files_in_directory(directory: str, log: logging.Logger) -> Optional[List[str]]:
    """
    Extracts a list of all files in a directory.

    :param directory: The directory to get files from.
    :param log: The configured logger to write to.

    :return: List of all files in the directory.
    """
    log.debug(f'Getting list of all files in directory: {directory}')
    files = []
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
        log.debug(f'Found {len(files)} files in directory: {directory}')
        return files
    except Exception as e:
        log.exception(str(e))
        raise FileException(str(e))

def rename_file(current_file_name: str, new_file_name: str, log: logging.Logger) -> bool:
    """
    Renames a file.

    :param current_file_name: The current file name.
    :param new_file_name: The new file name.
    :param log: The configured logger to write to.

    :return: True if the file was renamed, False otherwise.
    """
    log.debug(f'Renaming file: {current_file_name} to {new_file_name}')
    try:
        os.rename(current_file_name, new_file_name)
        log.debug(f'Successfully renamed file: {current_file_name} to {new_file_name}')
        return True
    except Exception as e:
        log.exception(str(e))
        raise FileException(str(e))

def rename_directory(current_directory_name: str, new_directory_name: str, log: logging.Logger) -> bool:
    """
    Renames a directory.

    :param current_directory_name: The current directory name.
    :param new_directory_name: The new directory name.
    :param log: The configured logger to write to.

    :return: True if the directory was renamed, False otherwise.
    """
    log.debug(f'Renaming directory: {current_directory_name} to {new_directory_name}')
    try:
        os.rename(current_directory_name, new_directory_name)
        log.debug(f'Successfully renamed directory: {current_directory_name} to {new_directory_name}')
        return True
    except Exception as e:
        log.exception(str(e))
        raise FileException(str(e))

def extract_file_extension(filename: str, log: logging.Logger) -> Optional[str]:
    """
    Extracts the file extension.

    :param filename: The filename.
    :param log: The configured logger to write to.

    :return: File extension.
    """
    log.debug(f'Getting file extension for file {filename}')
    try:
        extension = filename.split('.')[-1]
        if extension:
            log.debug(f'Found file extension for file {filename}. Extension: {extension}')
            return extension
        else:
            log.debug(f'Could not find file extension for file {filename}')
            return None
    except Exception as e:
        log.exception(str(e))
        raise FileException(str(e))
