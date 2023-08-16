from exceptions.wiggle_base_exception import WiggleGraphBaseException


class MakeClauseSyntaxError(WiggleGraphBaseException):
    pass


class MakeDuplicateHandlesError(WiggleGraphBaseException):
    pass


class MakeParamSyntaxError(WiggleGraphBaseException):
    pass


class MakeNonDirectedRelationshipError(WiggleGraphBaseException):
    pass


class MakeIllegalCharacterError(WiggleGraphBaseException):
    pass


class MakeRelationshipNameSyntaxError(WiggleGraphBaseException):
    pass


class UnNamedRelationShipError(WiggleGraphBaseException):
    pass


class MakeIllegalPropertyValue(WiggleGraphBaseException):
    pass


class MakePropertyTypeAssignmentError(WiggleGraphBaseException):
    pass
