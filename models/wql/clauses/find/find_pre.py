from typing import Optional

from pydantic import BaseModel, Field


class FindRelationshipPre(BaseModel):
    rel_name: Optional[str]
    rel_handle: Optional[str]
    props_dict_yes: Optional[dict] = Field(default=dict())
    props_dict_no: Optional[dict] = Field(default=dict())


class FindNodePre(BaseModel):
    node_label: str
    node_handle: Optional[str]
    props_dict_yes: Optional[dict] = Field(default=dict())
    props_dict_no: Optional[dict] = Field(default=dict())
    relationships: list[FindRelationshipPre] = Field(default=list())


class FindPre(BaseModel):
    left_node: FindNodePre
    middle_node: Optional[FindNodePre]
    right_node: Optional[FindNodePre]
    node_labels: set[str] = Field(default=set())
    relationship_names: set[Optional[str]] = Field(default=set())
