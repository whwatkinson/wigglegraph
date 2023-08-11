from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


TYPES_ALLOWED = Union[str, int, float, list]


# TODO MAKE A parent class for node and relationship
class Node(BaseModel):
    """
    The structure of the Node is Wiggle Graph.
    """

    # Internal
    wn: int
    node_label: str
    created_at: float = datetime.now().timestamp()
    updated_at: Optional[float] = None

    # User defined
    belongings: Optional[dict[str, TYPES_ALLOWED]] = None
    relations: Optional[list[str]] = None

    def __repr__(self) -> str:
        return f"{self.node_label}: {self.wn}"

    def export_node(self) -> dict:
        return {self.wn: self.dict()}
