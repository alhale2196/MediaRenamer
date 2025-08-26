
class MediaRenamerException(Exception):
    pass


class FileException(MediaRenamerException):
    def __init__(self, message):
        super(FileException, self).__init__(message)


class ParserException(MediaRenamerException):
    def __init__(self, message):
        super(ParserException, self).__init__(message)


class DirectoryScanException(MediaRenamerException):
    def __init__(self, message):
        super(DirectoryScanException, self).__init__(message)
