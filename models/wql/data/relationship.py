from typing import Any, Optional

from pydantic import BaseModel, root_validator

from exceptions.wql.data import RelationshipToFromError
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
        return self.relationship_metadata.wn

    def __repr__(self) -> str:
        return f"|{self.__class__.__name__}| {self.relationship_name}: FROM {self.wn_from_node} TO {self.wn_to_node}"

    def export_node(self) -> dict:
        return {self.relationship_metadata.wn: self.dict()}

    @root_validator
    def validate_from_to_wn(cls, values: dict) -> dict:
        wn_from_node = values["wn_from_node"]
        wn_to_node = values["wn_to_node"]

        if wn_from_node == wn_to_node:
            raise RelationshipToFromError(
                f"Self relationships are not allowed: WN{cls.wn} to: WN{wn_to_node} from: WN{wn_from_node}"
            )

        return values
