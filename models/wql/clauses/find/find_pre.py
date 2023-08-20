from typing import Optional

from pydantic import BaseModel


class NodeFindPre(BaseModel):
    node_label: str
    node_handle: Optional[str]
    props_dict: Optional[dict]
    criteria_dict: Optional[dict]
