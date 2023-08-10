import pytest

# from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.tests.cases_for_test_re import (
    cases_for_test_nodes_rel_pattern,
)
from wiggle_query_language.clauses.regexes.helpers import get_nodes_rels_pattern_regex
from wiggle_query_language.clauses.regexes.make import (
    NODES_RELS_PATTERN_REGEX,
)


class TestMakeRe:
    def test_get_pattern_regex(self) -> None:
        # regression test
        exp_pattern = r"\s*(?P<left_node>\(\s*(?P<left_node_handle>\w*)\s*:\s*(?P<left_node_label>\w+)\s*(?P<left_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?\s*(?P<left_middle_rel><?-\[\s*(?P<left_middle_rel_handle>\w*)\s*:\s*(?P<left_middle_rel_label>\w*)\s*(?P<left_middle_rel_props>[{}\w:\s,'\"\.\[\]@]+)?\s*]->?\s*)?\s*(?P<middle_node>\(\s*(?P<middle_node_handle>\w*)\s*:\s*(?P<middle_node_label>\w+)\s*(?P<middle_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?\s*(?P<middle_right_rel><?-\[\s*(?P<middle_right_rel_handle>\w*)\s*:\s*(?P<middle_right_rel_label>\w*)\s*(?P<middle_right_rel_props>[{}\w:\s,'\"\.\[\]@]+)?\s*]->?\s*)?\s*(?P<right_node>\(\s*(?P<right_node_handle>\w*)\s*:\s*(?P<right_node_label>\w+)\s*(?P<right_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?"
        test_pattern = rf"{get_nodes_rels_pattern_regex()}"

        assert test_pattern == exp_pattern

    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception", cases_for_test_nodes_rel_pattern
    )
    def test_nodes_rel_pattern_regex(
        self, test_pattern: str, expected_result: dict, exception
    ) -> None:
        test = [
            x.groupdict()
            for x in NODES_RELS_PATTERN_REGEX.finditer(test_pattern)
            if x.group()
        ]

        assert test == expected_result

    def test_make_statement_all_regex(self) -> None:
        pass

    @pytest.mark.xfail
    def test_make_statement_check_clause_syntax(self) -> None:
        pass

    @pytest.mark.xfail
    def test_make_statement_check_params_syntax(self) -> None:
        pass

    @pytest.mark.xfail
    def test_relationship_dir_check_regex(self) -> None:
        pass

    @pytest.mark.xfail
    def test_key_value_regex(self) -> None:
        pass

    @pytest.mark.xfail
    def test_list_key_value_regex(self) -> None:
        pass

    @pytest.mark.xfail
    def test_param_list_value(self) -> None:
        pass

    @pytest.mark.xfail
    def test_illegal_chars_regex(self) -> None:
        pass
