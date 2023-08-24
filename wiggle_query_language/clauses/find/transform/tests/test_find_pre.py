from typing import Generator

import pytest

from testing.test_helpers import does_not_raise
from models.wql import (
    FindNodePre,
    FindRelationshipPre,
    ParsedCriteria,
    Clause,
    ParsedCriteriaYesNo,
)
from wiggle_query_language.clauses.find.transform.find_pre import (
    add_criteria_yes_no_props,
)


class TestFindPre:
    @pytest.fixture
    def parse_criteria(self) -> Generator:
        props_dict_yes = {"int": 1}
        props_dict_no = {"str": "2"}
        criteria_handle_props = {
            "foo": ParsedCriteriaYesNo(
                props_dict_yes_match=props_dict_yes, props_dict_no_match=props_dict_no
            )
        }
        criteria = ParsedCriteria(
            raw_statement="foo",
            clause=Clause.CRITERIA,
            criteria_handle_props=criteria_handle_props,
        )

        yield criteria

    def test_add_criteria_add_props_node(
        self, parse_criteria: ParsedCriteria, exception=does_not_raise()
    ) -> None:
        with exception:
            before = FindNodePre(
                node_handle="foo",
                node_label="bar",
                props_dict_yes=dict(),
                props_dict_no=dict(),
                relationships=[],
            )

            test = add_criteria_yes_no_props(before, parse_criteria, before.node_handle)

            assert test.props_dict_yes["int"] == 1
            assert test.props_dict_no["str"] == "2"

    def test_add_criteria_add_props_relationship(
        self, parse_criteria: ParsedCriteria, exception=does_not_raise()
    ) -> None:
        with exception:
            before = FindRelationshipPre(
                rel_handle="foo",
                rel_name="bar",
                props_dict_yes=dict(),
                props_dict_no=dict(),
            )

            test = add_criteria_yes_no_props(before, parse_criteria, before.rel_handle)

            assert test.props_dict_yes["int"] == 1
            assert test.props_dict_no["str"] == "2"
