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


class EmitNodes(BaseModel):
    left: EmitNode
    middle: Optional[EmitNode]
    right: Optional[EmitNode]


class MakePre(BaseModel):
    left_node: Optional[NodePre]
    middle_node: Optional[NodePre]
    right_node: Optional[NodePre]
    left_middle_relationship: Optional[RelationshipPre]
    middle_right_relationship: Optional[RelationshipPre]

    def get_relationships(
        self, node_pre: NodePre, relationship_pre: RelationshipPre
    ) -> RelationshipPre:
        return (
            relationship_pre if relationship_pre.wn_from_node == node_pre.wn else None
        )

    def emit_nodes(self) -> EmitNodes:
        # TODO refactor this horrible mess, but it works for now... :P

        lm_rel = self.left_middle_relationship
        mr_rel = self.middle_right_relationship

        if lm_rel:
            left_node_rels = [
                rel
                for rel in [
                    lm_rel if lm_rel.wn_from_node == self.left_node.wn else None
                ]
                if rel
            ]
        else:
            left_node_rels = None
        left = EmitNode(node_pre=self.left_node, relationship_pre=left_node_rels)

        if self.middle_node:
            if lm_rel:
                lr = [
                    rel
                    for rel in [
                        lm_rel if lm_rel.wn_from_node == self.middle_node.wn else None
                    ]
                    if rel
                ]
            else:
                lr = []
            if mr_rel:
                rr = [
                    rel
                    for rel in [
                        mr_rel if mr_rel.wn_from_node == self.middle_node.wn else None
                    ]
                    if rel
                ]
            else:
                rr = []

            middle = EmitNode(
                node_pre=self.middle_node,
                relationship_pre=lr + rr,
            )
        else:
            middle = None

        if self.right_node:
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
        else:
            right = None

        return EmitNodes(left=left, middle=middle, right=right)
