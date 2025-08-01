import logging
import os
import sys

try:
    from .logfilters import SingleLevelFilter
except ImportError:
    sys.path.append('./')
    from logfilters import SingleLevelFilter


def get_configured_logger(name: str = None, log_level: str = 'INFO') -> logging.Logger:
    log = logging.getLogger(name or __name__)
    log.setLevel(log_level)
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')

    general_handler = logging.StreamHandler(sys.stdout)
    if log_level == 'DEBUG':
        general_filter = SingleLevelFilter(logging.DEBUG, False)
    else:
        general_filter = SingleLevelFilter(logging.INFO, False)
    general_handler.setFormatter(formatter)
    general_handler.addFilter(general_filter)
    log.addHandler(general_handler)

    error_handler = logging.StreamHandler(sys.stderr)
    error_filter = SingleLevelFilter(logging.WARNING)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(error_filter)
    log.addHandler(error_handler)
    log.propagate = False
    return log

def configure_logger(name: str = None, log_level: str = 'INFO', filters: list[logging.Filter] = []) -> logging.Logger:
    log = logging.getLogger(name or '')
    log.setLevel(log_level)
    log.handlers = []
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    general_handler = logging.StreamHandler(sys.stdout)
    general_handler.setFormatter(formatter)
    general_handler.setLevel(log_level)
    error_handler = logging.StreamHandler(sys.stderr)
    error_filter = SingleLevelFilter(logging.WARNING)
    error_handler.setFormatter(formatter)
    for fltr in filters:
        general_handler.addFilter(fltr)
        error_handler.addFilter((fltr))
    if log_level == 'DEBUG':
        general_handler.addFilter(SingleLevelFilter(logging.DEBUG, False))
    else:
        general_handler.addFilter(SingleLevelFilter(logging.INFO, False))
    error_handler.addFilter(SingleLevelFilter(logging.WARNING))
    log.addHandler(general_handler)
    log.addHandler(error_handler)
    return log


log = get_configured_logger(__name__)