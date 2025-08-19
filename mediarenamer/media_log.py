import logging

def media_log(log_level: str = 'INFO'):
    logging.basicConfig(level=log_level, format='[%(levelname)s]: %(message)s')

    log = logging.getLogger('media_log')
    return log
