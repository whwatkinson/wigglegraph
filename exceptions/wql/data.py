from exceptions.wiggle_base_exception import WiggleGraphBaseException


class RelationshipToFromError(WiggleGraphBaseException):
    pass


class NodeHasUnrelatedRelationship(WiggleGraphBaseException):
    pass
