from __future__ import print_function

import os
import sys
import argparse
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List

try:
    from .mediarenamer.version import __version__
    from .mediarenamer.exceptions import MediaRenamerException, FileException, ParserException
    from .mediarenamer.media_log import media_log
    from .mediarenamer.file_utils import write_to_file, extract_current_directory_basename, extract_list_of_folders_in_directory, \
        extract_list_of_files_in_directory, rename_file, rename_directory, extract_file_extension, delete_file, \
        parse_files_in_directory_to_delete, scan_directory, extract_directory_basename, extract_file_basename, \
        create_directory_for_movie_file, recursively_list_contents_in_directory
    from .mediarenamer.utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name, \
        extract_show_year_from_directory_name, extract_show_name_from_directory_basename, extract_movie_year_from_string
    from .mediarenamer.config import ALLOWED_FILE_EXTENSIONS
except ImportError:
    __version__ = 'development'
    sys.path.append('./')
    from mediarenamer.media_log import media_log
    from mediarenamer.exceptions import MediaRenamerException, FileException, ParserException
    from mediarenamer.file_utils import write_to_file, extract_current_directory_basename, extract_list_of_folders_in_directory, \
        extract_list_of_files_in_directory, rename_file, rename_directory, extract_file_extension, delete_file, \
        parse_files_in_directory_to_delete, scan_directory, extract_directory_basename, extract_file_basename, \
        create_directory_for_movie_file, recursively_list_contents_in_directory
    from mediarenamer.utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name, \
        extract_show_year_from_directory_name, extract_show_name_from_directory_basename, extract_movie_year_from_string
    from mediarenamer.config import ALLOWED_FILE_EXTENSIONS


MEDIA_FILE_EXTENSIONS = [
    'mp4',
    'mkv'
]

BANNED_FILE_EXTENSIONS = [
    'jpg'
]


def create_movie_dir_examples(movies_dir: str):
    out_data = {}
    example_names = []
    current_datetime = datetime.now().strftime('%Y%m%d-%H%M%S')
    out_data['datetime'] = current_datetime

    log = media_log(log_level='DEBUG')

    log.info('Creating example data file for movies directory...')

    try:
        directory_basename = extract_directory_basename(movies_dir)
        if not directory_basename:
            log.error('Failed to extract directory basename. Exiting...')
            exit(1)

        files = extract_list_of_files_in_directory(movies_dir)
        folders = extract_list_of_folders_in_directory(movies_dir)
        """
        contents = recursively_list_contents_in_directory(movies_dir)
        if not contents:
            log.error('Directory contents data list is empty. Exiting...')
            exit(1)
            
        files = contents['files']
        folders = contents['folders']
        """

        for file in files:
            file_basename = extract_file_basename(file)
            example_names.append(file_basename)

        for folder in folders:
            folder_basename = extract_directory_basename(folder)
            example_names.append(folder_basename)

        out_data['names'] = example_names

        contents = recursively_list_contents_in_directory(movies_dir)
        out_data['contents'] = contents

        outfile_path = Path("../data/movie-directory-examples.txt")
        if outfile_path.is_file():
            with open("../data/movie-directory-examples.json", "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
            json_file.close()
            dt = data['datetime']
            new_filename = f"../data/movie-directory-examples_{dt}.json"
            os.rename("../data/movie-directory-examples.json", new_filename)

        with open("../data/movie-directory-examples.json", "w") as f:
            json.dump(out_data, f, indent=4)


    except Exception as e:
        log.exception(str(e), exc_info=True)


def main():

    parser = argparse.ArgumentParser(
        description='A simple command line tool for media handling and processing for Plex library')

    parser.add_argument('-m', '--movie-dir', type=str, required=True, help='Directory with movie files')


    args = parser.parse_args()

    if args.movie_dir:
        create_movie_dir_examples(args.movie_dir)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
