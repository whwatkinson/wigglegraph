# import pytest
#
# from wiggle_query_language.clauses.regexes.make import (
#     NODES_RELS_PATTERN,
#     get_nodes_rels_pattern_regex,
# )
#
#
# class TestMakeRe:
#     def test_get_pattern_regex(self) -> None:
#         exp_pattern = r"\s*(?P<left_node>\(\s*(?P<left_node_handle>\w*)\s*:\s*(?P<left_node_label>\w+)\s*(?P<left_node_props>[{}\w:\s,'\".\[\]]+)?\s*\)\s*)?\s*(?P<left_middle_rel><?-\[\s*(?P<left_middle_rel_handle>\w*)\s*:\s*(?P<left_middle_rel_label>\w*)\s*(?P<left_middle_rel_props>[{}\w:\s,'\".\[\]]+)?\s*]->?\s*)?\s*(?P<middle_node>\(\s*(?P<middle_node_handle>\w*)\s*:\s*(?P<middle_node_label>\w+)\s*(?P<middle_node_props>[{}\w:\s,'\".\[\]]+)?\s*\)\s*)?\s*(?P<middle_right_rel><?-\[\s*(?P<middle_right_rel_handle>\w*)\s*:\s*(?P<middle_right_rel_label>\w*)\s*(?P<middle_right_rel_props>[{}\w:\s,'\".\[\]]+)?\s*]->?\s*)?\s*(?P<right_node>\(\s*(?P<right_node_handle>\w*)\s*:\s*(?P<right_node_label>\w+)\s*(?P<right_node_props>[{}\w:\s,'\".\[\]]+)?\s*\)\s*)"
#         test_pattern = rf"{get_nodes_rels_pattern_regex()}"
#
#         assert test_pattern == exp_pattern
#
#     def test_(self) -> None:
#         pass
