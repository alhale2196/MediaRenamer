from __future__ import print_function

import os
import sys
import argparse
import logging
from typing import Optional, List

try:
    from .version import __version__
    from .exceptions import MediaRenamerException, FileException, ParserException
    from .media_log import media_log
    from .file_utils import write_to_file, extract_current_directory_basename, extract_list_of_folders_in_directory, \
        extract_list_of_files_in_directory, rename_file, rename_directory, extract_file_extension, delete_file, \
        parse_files_in_directory_to_delete, scan_directory, extract_directory_basename, extract_file_basename, \
        create_directory_for_movie_file
    from .utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name, \
        extract_show_year_from_directory_name, extract_show_name_from_directory_basename, extract_movie_year_from_string
except ImportError:
    __version__ = 'development'
    sys.path.append('./')
    from media_log import media_log
    from exceptions import MediaRenamerException, FileException, ParserException
    from file_utils import write_to_file, extract_current_directory_basename, extract_list_of_folders_in_directory, \
        extract_list_of_files_in_directory, rename_file, rename_directory, extract_file_extension, delete_file, \
        parse_files_in_directory_to_delete, scan_directory, extract_directory_basename, extract_file_basename, \
        create_directory_for_movie_file
    from utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name, \
        extract_show_year_from_directory_name, extract_show_name_from_directory_basename, extract_movie_year_from_string


MEDIA_FILE_EXTENSIONS = [
    'mp4',
    'mkv'
]

BANNED_FILE_EXTENSIONS = [
    'jpg'
]


def run(debug: bool = False, dry_run: bool = False, verbose: bool = False, ignore_errors: bool = False, output_file: str = None):
    """

    :param debug:
    :param dry_run:
    :param verbose:
    :param ignore_errors:
    :param output_file:

    :return:
    """
    try:
        if debug:
            log = media_log(log_level='DEBUG')
        else:
            log = media_log(log_level='INFO')
    except Exception as e:
        raise MediaRenamerException(str(e))

    log.info('Starting media renamer...')
    log.debug(f'Debug mode: {debug}')
    log.debug(f'Dry run: {dry_run}')
    log.debug(f'Verbose mode: {verbose}')
    log.debug(f'Ignore errors: {ignore_errors}')
    if output_file:
        log.debug(f'Writing output to file: {output_file}')

    try:
        """
        Variables
        
        :var seasons:
        :var episodes:
        :var folders_to_rename:
        :var files_to_rename:
        :var files_to_delete:
        :var unknown_files:
        :var current_directory:
        """
        folders_to_rename = {}
        files_to_rename = {}
        files_to_delete = []
        master_unknown_folders = []
        master_unknown_files = []
        errored_folders = []
        errored_files = []

        current_directory = os.getcwd()

        if not current_directory:
            log.error('Failed to get current directory. Exiting...')
            exit(1)
        log.info(f'Current directory: {current_directory}')

        """
        
        """
        directory_basename = extract_directory_basename(current_directory)
        if not directory_basename:
            log.error('Failed to extract directory basename. Exiting...')
            exit(1)
        if directory_basename == "Movie":
            log.debug('Movie directory detected')
        elif directory_basename == "TV":
            log.debug('TV directory detected')
        else:
            log.error('Unknown media directory detected. Exiting...')
            exit(1)
        files = extract_list_of_files_in_directory(current_directory)
        folders = extract_list_of_folders_in_directory(current_directory)

        if directory_basename == 'Movie':
            for file in files:
                file_extension = extract_file_extension(file)
                if file_extension:
                    if file_extension == 'parts':
                        continue
                log.debug(f'Creating directory for file: {file}...')
                new_directory = create_directory_for_movie_file(file)
                if not new_directory:
                    log.warning(f'Failed to create directory for file: {file}')
                else:
                    log.debug(f'Created directory for file: {file}. Directory: {new_directory}')
                    folders.append(new_directory)

            for folder in folders:
                folder_basename = extract_directory_basename(folder)
                if not folder_basename:
                    log.warning(f'Failed to extract directory basename for folder: {folder}')
                    continue
                movie_year = extract_movie_year_from_string(folder_basename)
                if not movie_year:
                    log.warning(f'Failed to extract movie year for folder: {folder}')
                    continue
                movie_title = folder_basename.split(movie_year)[0]
                if not movie_title:
                    log.warning(f'Failed to extract movie title for folder: {folder}')
                    continue
                movie_title = movie_title.replace('(', ' ')
                movie_title = movie_title.replace(')', ' ')
                movie_title = movie_title.replace('.', ' ')
                new_folder_name = f'{movie_title} ({movie_year})'
                new_folder = os.path.join(current_directory, new_folder_name)
                log.debug(f'Renaming directory: {folder} to {new_folder}...')
                if not dry_run:
                    if not rename_directory(folder, new_folder):
                        log.warning(f'Failed to rename directory for folder: {folder}')
                        continue
                else:
                    new_folder = folder

                log.debug(f'Extracting files in directory: {new_folder}...')
                files_in_directory = extract_list_of_files_in_directory(new_folder)
                folders_in_directory = extract_list_of_folders_in_directory(new_folder)

                if not files_in_directory:
                    log.debug(f'No files in directory: {new_folder}')
                else:
                    for file in files_in_directory:
                        file_extension = extract_file_extension(file)
                        if not file_extension:
                            log.warning(f'Failed to extract file extension for file: {file}')
                            continue
                        if file_extension in BANNED_FILE_EXTENSIONS:
                            log.debug(f'Detected banned file extension for file: {file}')
                            if not dry_run:
                                delete_file(file)
                        elif file_extension in MEDIA_FILE_EXTENSIONS:
                            log.debug(f'Detected media file extension for file: {file}')
                            folder_basename = extract_directory_basename(new_folder)
                            new_file_name = f'{folder_basename}.{file_extension}'
                            new_file = os.path.join(new_folder, new_file_name)
                            log.debug(f'Renaming file: {file} to {new_file}...')
                            if not dry_run:
                                if not rename_file(file, new_file_name):
                                    log.warning(f'Failed to rename file {file} to {new_file_name}')
                                    continue
                        else:
                            log.warning(f'Failed to detect file type for file: {file}')

                if not folders_in_directory:
                    log.debug(f'No folders in directory: {new_folder}')
                else:
                    for folder in folders_in_directory:
                        folder_basename = extract_directory_basename(folder)
                        if not folder_basename:
                            log.warning(f'Failed to extract folder basename for folder: {folder}')
                            continue
                        if folder_basename == 'Featurettes':
                            log.debug(f'Detected featurettes folder in folder: {folder}')
                            files_in_featurettes = extract_list_of_files_in_directory(folder)
                            folders_in_featurettes = extract_list_of_folders_in_directory(folder)
                            for file_in_featurettes in files_in_featurettes:
                                file_extension = extract_file_extension(file_in_featurettes)
                                if not file_extension:
                                    log.warning(f'Failed to extract file extension for file: {file_in_featurettes}')
                                    continue
                                if file_extension in BANNED_FILE_EXTENSIONS:
                                    log.debug(f'Detected banned file extension for file: {file_in_featurettes}')
                                    if not dry_run:
                                        delete_file(file_in_featurettes)
                                elif file_extension in MEDIA_FILE_EXTENSIONS:
                                    log.debug(f'Detected media file extension for file: {file_in_featurettes}')
                                else:
                                    log.warning(f'Failed to detect file type for file: {file_in_featurettes}')
                        elif folder_basename == 'Subs':
                            log.debug(f'Detected subs folder in folder: {folder}')
                            files_in_subs = extract_list_of_files_in_directory(folder)
                            folders_in_subs = extract_list_of_folders_in_directory(folder)
                            for file_in_subs in files_in_subs:
                                file_extension = extract_file_extension(file_in_subs)
                                if not file_extension:
                                    log.warning(f'Failed to extract file extension for file: {file_in_subs}')
                                    continue
                                elif file_extension == 'srt':
                                    log.debug(f'Found subtitle file: {file_in_subs}')
                                    continue
                                else:
                                    log.warning(f'Failed to detect file type for file: {file_in_subs}')

        log.info('Complete!')

    except Exception as e:
        log.exception(MediaRenamerException(str(e)))


def run_media_info(debug:bool = False, verbose:bool = False):
    """
    The run media info run type function.

    :param debug: Is debug enabled.
    :param verbose: Is verbose enabled.
    """
    try:
        if debug:
            log = media_log(log_level='DEBUG')
        else:
            log = media_log(log_level='INFO')
    except Exception as e:
        raise MediaRenamerException(str(e))

    log.info('Getting media info for current directory...')
    try:
        seasons = {}
        episodes = {}

        current_directory = os.getcwd()

        directory_basename = extract_current_directory_basename()
        if not directory_basename:
            log.error('Failed to get directory basename.')
            return

        show_year = extract_show_year_from_directory_name(directory_basename)
        show_name = directory_basename.replace(show_year, '')
        if not show_name:
            log.error('Failed to get show name.')
            return

        folders_in_directory = extract_list_of_folders_in_directory(current_directory)
        files_in_directory = extract_list_of_files_in_directory(current_directory)

        if folders_in_directory:
            log.info(f'Extracting season folders for show: {show_name}...')
            for folder_in_directory in folders_in_directory:
                season_number = extract_season_number_from_directory_name(folder_in_directory)
                if season_number:
                    seasons[folder_in_directory] = season_number
            log.info(f'Extracted {len(seasons)} season folders for show: {show_name}')
        else:
            log.info(f'No season folders found for show: {show_name}')

        if files_in_directory:
            files_to_delete = parse_files_in_directory_to_delete(files_in_directory)

        if files_in_directory:
            log.info(f'Extracting episode files for show: {show_name}...')
            for file_in_directory in files_in_directory:
                episode_number = extract_episode_number_from_file_name(file_in_directory)
                if episode_number:
                    episodes[file_in_directory] = episode_number
            log.info(f'Extracted {len(episodes)} episode files for show: {show_name}')
        else:
            log.info(f'No episode files found for show: {show_name}')

    except Exception as e:
        log.exception(MediaRenamerException(str(e)))


def run_movie(debug: bool = False, dry_run: bool = False, verbose: bool = False, ignore_errors: bool = False, output_file: str = None):
    if extract_current_directory_basename() != "Movie":
        print("Not in movie directory. Exiting...")
        exit(1)

    try:
        pass

    except Exception as e:
        print(e)
        exit(1)


def run_tv(debug: bool = False, dry_run: bool = False, verbose: bool = False, ignore_errors: bool = False, output_file: str = None):
    pass


def test_run():
    print(extract_current_directory_basename())


def main():
    VERBOSE = False
    IGNORE_ERRORS = False
    WRITE_TO_FILE = False
    FILENAME_TO_WRITE = None
    DEBUG = False
    DRY_RUN = False

    parser = argparse.ArgumentParser(description='A simple command line tool for media handling and processing for Plex library')

    general_group = parser.add_argument_group('General Options')
    general_group.add_argument('--verbose', action='store_true', help='Enable verbose output')
    general_group.add_argument('--version', action='store_true', help='Print program version and exit')
    general_group.add_argument('-U', '--update', action='store_true', help='Update this program to latest version. Make sure that you have sufficient permissions (run with sudo if needed)')
    general_group.add_argument('-i', '--ignore-errors', action='store_true', help='Dont exit the program on error and keep processing files')
    general_group.add_argument('--output-file', help='File to save previous directory/file names and new names')
    general_group.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')

    run_option_group = parser.add_argument_group('Run Options')
    run_option_group.add_argument('-r', '--run', action='store_true', help='Run the program')
    run_option_group.add_argument('-m', '--media-info', action='store_true', help='Show media info generated for current directory')
    run_option_group.add_argument('-t', '--test', action='store_true', help='Run tests')
    run_option_group.add_argument('--dry-run', action='store_true', help='Run program like normal but dont alter any directories or files')

    args = parser.parse_args()

    if args.verbose:
        VERBOSE = True
    if args.ignore_errors:
        IGNORE_ERRORS = True
    if args.output_file:
        WRITE_TO_FILE = True
        FILENAME_TO_WRITE = args.output_file
    if args.debug:
        DEBUG = True
    if args.dry_run:
        DRY_RUN = True


    if args.run:
        if WRITE_TO_FILE:
            run(DEBUG, DRY_RUN, VERBOSE, IGNORE_ERRORS, FILENAME_TO_WRITE)
        else:
            run(DEBUG, DRY_RUN, VERBOSE, IGNORE_ERRORS)

    elif args.media_info:
        run_media_info(DEBUG, VERBOSE)

    elif args.test:
        test_run()

    elif args.version:
        if __version__ == 'development':
            print('MediaRenamer Development Version')
        else:
            print(f'MediaRenamer v{__version__}')
        return

    elif args.update:
        print('Update function not currently implemented.')
        return

    else:
        parser.print_help()


if __name__ == '__main__':
    main()