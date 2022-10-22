from exceptions.exception_base import WiggleGraphBaseException


class Statement(WiggleGraphBaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
