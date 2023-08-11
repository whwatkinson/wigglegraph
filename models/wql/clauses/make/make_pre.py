from typing import Optional

from pydantic import BaseModel


class NodePre(BaseModel):
    wn: int
    node_label: str
    node_handle: Optional[str]
    props_string: Optional[str]


class RelationshipPre(BaseModel):
    wn: int
    rel_name: Optional[str]
    rel_handle: Optional[str]
    props_string: Optional[str]
    wn_from_node: int
    wn_to_node: int


class MakePre(BaseModel):
    left_node: Optional[NodePre]
    middle_node: Optional[NodePre]
    right_node: Optional[NodePre]
    left_middle_relationship: Optional[RelationshipPre]
    middle_right_relationship: Optional[RelationshipPre]
