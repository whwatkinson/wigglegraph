from exceptions.wiggle_base_exception import WiggleGraphBaseException


class WiggleGraphIllegalPropertyValue(WiggleGraphBaseException):
    pass


class PropertyTypeAssignmentError(WiggleGraphBaseException):
    pass


class ClauseSyntaxError(WiggleGraphBaseException):
    pass


class IllegalCharacterError(WiggleGraphBaseException):
    pass


class NonDirectedRelationshipError(WiggleGraphBaseException):
    pass


class ParamSyntaxError(WiggleGraphBaseException):
    pass


class RelationshipNameSyntaxError(WiggleGraphBaseException):
    pass
