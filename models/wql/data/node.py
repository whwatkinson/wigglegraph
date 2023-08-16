from typing import Any, Optional

from pydantic import BaseModel, root_validator

from exceptions.wql.data import NodeHasUnrelatedRelationship

# from models.wql.data import WG_ALLOWED_TYPES
from models.wql.data.relationship import Relationship
from models.wql.data.wiggle_metadata import WiggleGraphMetalData


class Node(BaseModel):
    """
    The structure of the Node in Wiggle Graph.
    """

    # Internal
    node_metadata: WiggleGraphMetalData

    # User defined
    node_label: str
    # Using WG_ALLOWED_TYPES marshals the data incorrectly
    properties: Optional[dict[str, Any]] = None
    relations: Optional[list[Relationship]] = None

    @property
    def wn(self):
        return self.node_metadata.wn

    def __repr__(self) -> str:
        return f"|{self.__class__.__name__}| {self.node_label}: {self.node_metadata.wn}"

    def export_node(
        self, exclude_unset: bool = False, exclude_none: bool = False
    ) -> dict[str, dict[str, Any]]:
        return {
            str(self.node_metadata.wn): self.dict(
                exclude_unset=exclude_unset, exclude_none=exclude_none
            )
        }

    def export_relationship_indexes(self) -> Optional[dict[str, set[int]]]:
        if self.relations:
            return {
                str(self.node_metadata.wn): {
                    relationship.wn_to_node for relationship in self.relations
                }
            }
        return None

    @root_validator
    def validate_relationships(cls, values: dict) -> dict:
        node_metadata = values["node_metadata"]
        relations = values["relations"]

        if relations:
            for relationship in relations:
                if node_metadata.wn not in (
                    relationship.wn_from_node,
                    relationship.wn_to_node,
                ):
                    raise NodeHasUnrelatedRelationship(
                        f"Relationship WN{relationship.relationship_metadata.wn} not associated with this node."
                    )

        return values
