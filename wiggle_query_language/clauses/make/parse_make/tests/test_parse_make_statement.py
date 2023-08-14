import pytest

from exceptions.wql.make import MakeClauseSyntaxError
from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_statement import (
    build_parsed_make,
    extract_all_make_statements,
    parse_make_statement_from_query_string,
)


class TestWqlMake:
    @pytest.mark.parametrize(
        "test_query, expected_output, exception",
        [
            pytest.param(
                "MAKE (:NodeLabel);",
                ["MAKE (:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Simple Case",
            ),
            pytest.param(
                "MAKE (node1:NodeLabel);",
                ["MAKE (node1:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Simple Case with label",
            ),
            pytest.param(
                "MAKE (:NodeLabel)-[:]->(:NodeLabel);",
                ["MAKE (:NodeLabel)-[:]->(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Double Node with right direction",
            ),
            pytest.param(
                "MAKE (:NodeLabel)<-[:]-(:NodeLabel);",
                ["MAKE (:NodeLabel)<-[:]-(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Double Node with left direction",
            ),
            pytest.param(
                "MAKE (:NodeLabel)-[:REL]->(:NodeLabel);",
                ["MAKE (:NodeLabel)-[:REL]->(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Double Node with right direction and named rel",
            ),
            pytest.param(
                "MAKE (:NodeLabel)-[rel1:REL]->(:NodeLabel);",
                ["MAKE (:NodeLabel)-[rel1:REL]->(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Double Node with right direction, named and labeled rel",
            ),
            pytest.param(
                "MAKE (node1:NodeLabel)-[rel1:REL]->(:NodeLabel);",
                ["MAKE (node1:NodeLabel)-[rel1:REL]->(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Left Node labeled with right direction, named and labeled rel",
            ),
            pytest.param(
                "MAKE (:NodeLabel)-[rel1:REL]->(node2:NodeLabel);",
                ["MAKE (:NodeLabel)-[rel1:REL]->(node2:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Right Node labeled with right direction, named and labeled rel",
            ),
            pytest.param(
                "MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);",
                ["MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: All labels",
            ),
            pytest.param(
                (
                    """MAKE (n:NodeLabel)-[r:REL]->(n:NodeLabel);
                    FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
                    CRITERIA p.name = 'Bar' or q.name = 'Bar';
                    REPORT wn(p), wn(q);"""
                ),
                ["MAKE (n:NodeLabel)-[r:REL]->(n:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Multi Stage Query",
            ),
            pytest.param(
                """
                MAKE (:NodeLabel);
                MAKE (:NodeLabel);
                """,
                ["MAKE (:NodeLabel);", "MAKE (:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Simple Case",
            ),
        ],
    )
    def test_extract_all_make_statements__basic_pattern_matching(
        self, test_query: str, expected_output: list[str], exception
    ) -> None:
        with exception:
            test = extract_all_make_statements(test_query)
            assert test == expected_output

    @pytest.mark.parametrize(
        "test_make_stmt, expected_value, exception",
        [
            pytest.param(
                "MAKE (:NodeLabel)-[:]->(:NodeLabel);",
                {"left_node_label": "NodeLabel", "middle_node_label": "NodeLabel"},
                does_not_raise(),
                id="EXP PASS: Simple case",
            ),
            pytest.param(
                "MAKE (foo:NodeLabel{int: 1, str: '2', none: null, bool: true})-[:]->(foo2:NodeLabel);",
                {
                    "left_node_handle": "foo",
                    "left_node_props": "{int: 1, str: '2', none: null, bool: true}",
                    "middle_node_handle": "foo2",
                },
                does_not_raise(),
                id="EXP PASS: NodeHandles, NodeLabels and NodeParams",
            ),
            pytest.param(
                """MAKE (:NodeLabel)-[r:REL{float: 3.14, none: null, list: [1, '2', "2_4", "3 4", 3.14]}]->(:NodeLabel);""",
                {
                    "left_middle_rel_handle": "r",
                    "left_middle_rel_label": "REL",
                    "left_middle_rel_props": """{float: 3.14, none: null, list: [1, '2', "2_4", "3 4", 3.14]}""",
                },
                does_not_raise(),
                id="EXP PASS: RelHandles, RelLabels and RelParams",
            ),
        ],
    )
    def test_build_parsed_make(
        self, test_make_stmt: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = build_parsed_make(test_make_stmt)

            test_parsed_make = test.parsed_pattern_list[0]

            for test_key, test_value in expected_value.items():
                assert getattr(test_parsed_make, test_key) == test_value

    @pytest.mark.parametrize(
        "test_make_stmt, expected_value, exception",
        [
            pytest.param(
                "MAKE (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);",
                1,
                does_not_raise(),
                id="EXP PASS: Simple case",
            ),
            pytest.param(
                "FIND (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);",
                0,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC: Not a MAKE stmt",
            ),
            pytest.param(
                "MAEK (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);",
                0,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC: MAKE clause sp error",
            ),
        ],
    )
    def test_extract_make_statement_from_query(
        self, test_make_stmt: str, expected_value: None, exception
    ) -> None:
        with exception:
            test = parse_make_statement_from_query_string(test_make_stmt)
            assert len(test) == 1
