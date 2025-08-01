from __future__ import print_function

import os
import sys
import argparse

try:
    from .version import __version__
    from .exceptions import MediaRenamerException
    from .media_log import get_configured_logger
    from .file_utils import write_to_file, extract_current_directory_basename, extract_list_of_folders_in_directory, \
        extract_list_of_files_in_directory, rename_file, rename_directory, extract_file_extension
    from .utils import extract_season_number_from_directory_name, extract_episode_number_from_file_name, extract_show_year_from_directory_name
except ImportError:
    __version__ = 'development'
    sys.path.append('./')
    from media_log import get_configured_logger
    from exceptions import MediaRenamerException
    from file_utils import write_to_file, get_current_directory_basename, get_list_of_folders_in_directory, \
        get_list_of_files_in_directory, rename_file, rename_directory, get_file_extension
    from utils import get_season_number_from_folder_name, get_episode_number_from_file_name, extract_show_year_from_directory_name


def run(debug: bool = False, dry_run: bool = False, verbose: bool = False, ignore_errors: bool = False, output_file: str = None):
    pass


def run_media_info(debug:bool = False, verbose:bool = False):
    """
    The run media info run type function.

    :param debug: Is debug enabled.
    :param verbose: Is verbose enabled.
    """
    try:
        if debug:
            log = get_configured_logger(__name__, log_level='DEBUG')
        else:
            log = get_configured_logger(__name__, log_level='INFO')
    except Exception as e:
        raise MediaRenamerException(str(e))

    log.info('Getting media info for current directory...')
    try:
        directory_basename = get_current_directory_basename(log)
        if not directory_basename:
            log.error('Failed to get directory basename.')
    except Exception as e:
        log.exception(MediaRenamerException(str(e)))


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