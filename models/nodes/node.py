from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


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
    belongings: Optional[dict[str, Any]] = None
    relations: Optional[list[str]] = None

    def __repr__(self) -> str:
        return f"{self.node_label}: {self.wn}"

    def export_node(self) -> dict:

        return {self.wn: self.dict()}
