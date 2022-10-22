from exceptions.exception_base import WiggleGraphBaseException


class StatementError(WiggleGraphBaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class IllegalParameterType(WiggleGraphBaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
