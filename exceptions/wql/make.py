from exceptions.wiggle_base_exception import WiggleGraphBaseException


class MakeClauseSyntaxError(WiggleGraphBaseException):
    pass


class MakeParamSyntaxError(WiggleGraphBaseException):
    pass


class MakeNonDirectedRelationshipError(WiggleGraphBaseException):
    pass


class MakeIllegalCharacterError(WiggleGraphBaseException):
    pass
