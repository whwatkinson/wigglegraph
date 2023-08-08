from exceptions.wql.wqlbase import WqlException


class MakeClauseSyntaxError(WqlException):
    pass


class MakeParamSyntaxError(WqlException):
    pass


class MakeNonDirectedRelationshipError(WqlException):
    pass
