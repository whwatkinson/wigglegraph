from typing import Optional

from pydantic import BaseModel, Field


class RelationshipPre(BaseModel):
    wn: int
    rel_name: Optional[str]
    rel_handle: Optional[str]
    props_string: Optional[str]
    wn_from_node: Optional[int]
    wn_to_node: Optional[int]


class NodePre(BaseModel):
    wn: int
    node_label: str
    node_handle: Optional[str]
    props_string: Optional[str]
    relationships_pre: list[RelationshipPre] = Field(default_factory=list)


class MakePre(BaseModel):
    left_node: NodePre
    middle_node: Optional[NodePre]
    right_node: Optional[NodePre]
    node_labels: set[str] = Field(default_factory=set)
    relationship_names: set[Optional[str]] = Field(default_factory=set)
