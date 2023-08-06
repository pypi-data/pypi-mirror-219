from typing import Optional

STATUS_CODE_400: int = 400


class InstagraderException(Exception):
    error_message: str = ''
    status_code: int = STATUS_CODE_400

    def __init__(self, error_message: Optional[str] = None):
        if error_message:
            self.error_message = error_message


class InvalidInputException(InstagraderException):
    pass


class ResourceNotFoundException(InstagraderException):
    pass


class AccessDeniedException(InstagraderException):
    pass


class ConflictException(InstagraderException):
    pass


class ExpiredAccountException(InstagraderException):
    pass


class MaxAttemptsReachedException(InstagraderException):
    pass


class InternalServerException(InstagraderException):
    pass


def raise_exception(exception_name: str, exception_message: str):
    if exception_name == InvalidInputException.__name__:
        raise InvalidInputException(exception_message)
    if exception_name == ResourceNotFoundException.__name__:
        raise ResourceNotFoundException(exception_message)
    if exception_name == AccessDeniedException.__name__:
        raise AccessDeniedException(exception_message)
    if exception_name == ConflictException.__name__:
        raise ConflictException(exception_message)
    if exception_name == ExpiredAccountException.__name__:
        raise ExpiredAccountException(exception_message)
    if exception_name == MaxAttemptsReachedException.__name__:
        raise MaxAttemptsReachedException(exception_message)
    if exception_name == InternalServerException.__name__:
        raise InternalServerException(exception_message)
