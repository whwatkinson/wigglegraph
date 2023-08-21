from typing import Optional

from pydantic import BaseModel, Field


class FindRelationshipPre(BaseModel):
    rel_name: Optional[str]
    rel_handle: Optional[str]
    props_dict: Optional[dict]


class FindNodePre(BaseModel):
    node_label: str
    node_handle: Optional[str]
    props_dict: Optional[dict]
    relationships: list[FindRelationshipPre] = Field(default=[])


class FindPre(BaseModel):
    left_node: Optional[FindNodePre]
    middle_node: Optional[FindNodePre]
    right_node: Optional[FindNodePre]
