from typing import Optional

from pydantic import BaseModel


class NodeFindPre(BaseModel):
    node_label: str
    node_handle: Optional[str]
    props_string: Optional[str]
