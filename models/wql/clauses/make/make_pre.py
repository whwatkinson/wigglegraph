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

    def emit_node_rels(self) -> tuple:
        # TODO make this a model not a tuple

        lm_rel = self.left_middle_relationship
        mr_rel = self.middle_right_relationship

        return (
            (
                self.left_node,
                lm_rel if lm_rel.wn_from_node == self.left_node.wn else None,
            ),
            (
                self.middle_node,
                lm_rel if lm_rel.wn_from_node == self.middle_node.wn else None,
                mr_rel if mr_rel.wn_from_node == self.middle_node.wn else None,
            ),
            (
                self.right_node,
                mr_rel if mr_rel.wn_from_node == self.right_node.wn else None,
            ),
        )
