import pytest

from exceptions.wql.parsing import ClauseSyntaxError
from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_statement import (
    build_parsed_make,
    parse_make_statement_from_query_string,
)


class TestParseMake:
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
                """
                MAKE (n:NodeLabel)-[r:REL]->(m:NodeLabel);
                ADJUST n.name = "h" and m.name = "Wig";
                FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
                CRITERIA p.name = "Bar" or q.name = "Bar;
                REPORT wn(p), wn(q);
                """,
                1,
                does_not_raise(),
                id="EXP PASS: Multiline query",
            ),
            pytest.param(
                """
                MAKE (n:NodeLabel)-[r:REL]->(m:NodeLabel);
                MAKE (n:NodeLabel2)-[r:REL]->(m:NodeLabel2);
                ADJUST n.name = "h" and m.name = "Wig";
                FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
                CRITERIA p.name = "Bar" or q.name = "Bar;
                REPORT wn(p), wn(q);
                """,
                2,
                does_not_raise(),
                id="EXP PASS: Multiline query, two MAKES",
            ),
            pytest.param(
                """
                MAKE (n:NodeLabel)-[r:REL]->(m:NodeLabel), (n:NodeLabel2)-[r:REL]->(m:NodeLabel2);
                ADJUST n.name = "h" and m.name = "Wig";
                FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
                CRITERIA p.name = "Bar" or q.name = "Bar;
                REPORT wn(p), wn(q);
                """,
                1,
                does_not_raise(),
                id="EXP PASS:  Multiline query, One make, two patterns",
            ),
            pytest.param(
                "FIND (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);",
                None,
                does_not_raise(),
                id="EXP PASS: Not a MAKE stmt",
            ),
            pytest.param(
                "MAEK (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);",
                0,
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: MAKE clause sp error",
            ),
        ],
    )
    def test_extract_make_statement_from_query(
        self, test_make_stmt: str, expected_value: None, exception
    ) -> None:
        with exception:
            test = parse_make_statement_from_query_string(test_make_stmt)
            if test:
                assert len(test) == expected_value
            else:
                assert test is None
