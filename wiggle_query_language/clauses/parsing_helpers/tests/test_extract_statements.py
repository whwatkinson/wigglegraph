import pytest

from models.wql import Clause
from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.parsing_helpers.extract_statements import (
    extract_all_statements,
)


class TestExtractStatements:
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
    def test_extract_all_make_statements(
        self, test_query: str, expected_output: list[str], exception
    ) -> None:
        with exception:
            test = extract_all_statements(test_query, Clause.MAKE)
            assert test == expected_output
