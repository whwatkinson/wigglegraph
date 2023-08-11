from typing import Optional

from pydantic import BaseModel


class NodePre(BaseModel):
    wn: int
    node_label: str
    handle: Optional[str]
    wn_of_rel_to: Optional[int]
    props_str: Optional[str]


class RelationshipPre(BaseModel):
    wn: int
    rel_name: str
    handle: Optional[str]
    props_str: Optional[str]


class MakePre(BaseModel):
    left_node: Optional[NodePre]
    middle_node: Optional[NodePre]
    right_node: Optional[NodePre]

    left_middle_relationship: Optional[RelationshipPre]
    middle_right_relationship: Optional[RelationshipPre]
