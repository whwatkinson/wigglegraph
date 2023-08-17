from exceptions.wiggle_base_exception import WiggleGraphBaseException


class MakeClauseSyntaxError(WiggleGraphBaseException):
    pass


class MakeDuplicateHandlesError(WiggleGraphBaseException):
    pass


class MakeParamSyntaxError(WiggleGraphBaseException):
    pass


class MakeRelationshipNameSyntaxError(WiggleGraphBaseException):
    pass
