from typing import Optional, Any

from pydantic import BaseModel, root_validator

from models.wql.data.wiggle_metadata import WiggleGraphMetalData

# from models.wql.data import WG_ALLOWED_TYPES


class Relationship(BaseModel):

    """
    The structure of the Relationship in Wiggle Graph.
    """

    # Internal
    relationship_metadata: WiggleGraphMetalData

    # User defined
    relationship_name: Optional[str]
    wn_from_node: int
    wn_to_node: int
    # Using WG_ALLOWED_TYPES marshals the data incorrectly
    properties: Optional[dict[str, Any]] = None

    @property
    def wn(self):
        return self.rel_metadata.wn

    def __repr__(self) -> str:
        return f"|{self.__class__.__name__}| {self.relationship_name}: FROM {self.wn_from_node} TO {self.wn_to_node}"

    def export_node(self) -> dict:
        return {self.rel_metadata.wn: self.dict()}

    @root_validator
    def validate_from_to_wn(cls, values: dict) -> dict:
        if values["wn_from_node"] == values["wn_to_node"]:
            # TODO custom exec
            raise Exception("from == to")

        return values
