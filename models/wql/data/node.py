from typing import Optional, Any


from models.wql.data.wiggle_metadata import WiggleGraphMetalData

# from models.wql.data import TYPES_ALLOWED
from models.wql.data.relationship import Relationship

from pydantic import BaseModel


class Node(BaseModel):
    """
    The structure of the Node in Wiggle Graph.
    """

    # Internal
    node_metadata: WiggleGraphMetalData

    # User defined
    node_label: str
    # Using types allowed marshals the data incorrectly
    properties: Optional[dict[str, Any]] = None
    relations: Optional[list[Relationship]] = None

    @property
    def wn(self):
        return self.node_metadata.wn

    def __repr__(self) -> str:
        return f"|{self.__class__.__name__}| {self.node_label}: {self.node_metadata.wn}"

    def export_node(self) -> dict:
        return {self.node_metadata.wn: self.dict()}
