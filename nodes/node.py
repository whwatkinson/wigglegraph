from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class Node(BaseModel):
    # Internal
    wiggle_number: int
    node_label: str
    created_at: float = datetime.now().timestamp()
    updated_at: Optional[float] = None

    # User defined
    belongings: Optional[dict[str, Any]] = None
    relations: Optional[list[str]] = None

    def __repr__(self) -> str:
        return f"{self.node_label}: {self.wiggle_number}"

    def export_node(self) -> dict:

        return {self.wiggle_number: self.dict()}
