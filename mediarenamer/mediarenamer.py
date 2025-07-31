from __future__ import print_function

import os
import sys
import argparse

try:
    from .version import __version__
except ImportError:
    __version__ = 'development'

try:
    from .file_utils import (
        write_to_file,
        get_current_directory_basename,
    )
except ImportError:
    sys.path.append('./')
    from file_utils import (
        write_to_file,
        get_current_directory_basename,
    )

VERBOSE = False
VERSION = __version__
IGNORE_ERRORS = False
WRITE_TO_FILE = False
FILENAME_TO_WRITE = None
DEBUG = False
DRY_RUN = False


def run():
    pass

def main():
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
        pass
    elif args.media_info:
        pass
    elif args.version:
        if VERSION == 'development':
            print('MediaRenamer Development Version')
        else:
            print(f'MediaRenamer v{VERSION}')
        return
    elif args.update:
        print('Update function not currently implemented.')
        return
    else:
        parser.print_help()


if __name__ == '__main__':
    main()