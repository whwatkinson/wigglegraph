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
    wn_from_node: Optional[int]
    wn_to_node: Optional[int]


class EmitNode(BaseModel):
    node_pre: Optional[NodePre]
    relationship_pre: Optional[list[RelationshipPre]]


class EmitNodesPre(BaseModel):
    left: EmitNode
    middle: Optional[EmitNode]
    right: Optional[EmitNode]


class MakePre(BaseModel):
    left_node: Optional[NodePre]
    middle_node: Optional[NodePre]
    right_node: Optional[NodePre]
    left_middle_relationship: Optional[RelationshipPre]
    middle_right_relationship: Optional[RelationshipPre]

    def get_node_rels(self, node: NodePre, relationship: RelationshipPre):
        rel = relationship if relationship.wn_from_node == node.wn else None
        return rel

    def emit_nodes(self) -> EmitNodesPre:
        # TODO refactor this horrible mess, but it works :P

        lm_rel = self.left_middle_relationship
        mr_rel = self.middle_right_relationship

        left_node_rels = [
            rel
            for rel in [lm_rel if lm_rel.wn_from_node == self.left_node.wn else None]
            if rel
        ]
        left = EmitNode(node_pre=self.left_node, relationship_pre=left_node_rels)
        middle = EmitNode(
            node_pre=self.middle_node,
            relationship_pre=[
                rel
                for rel in [
                    lm_rel if lm_rel.wn_from_node == self.middle_node.wn else None,
                    mr_rel if mr_rel.wn_from_node == self.middle_node.wn else None,
                ]
                if rel
            ],
        )
        right = EmitNode(
            node_pre=self.right_node,
            relationship_pre=[
                rel
                for rel in [
                    mr_rel if mr_rel.wn_from_node == self.right_node.wn else None,
                ]
                if rel
            ],
        )

        return EmitNodesPre(left=left, middle=middle, right=right)
