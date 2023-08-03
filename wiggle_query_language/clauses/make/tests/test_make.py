from contextlib import contextmanager
from typing import Generator

import pytest

from wiggle_query_language.clauses.make.make import extract_make_statement_from_query


@contextmanager
def does_not_raise() -> Generator:
    yield None


class TestWqlMake:
    @pytest.mark.parametrize(
        "sample_query, expected_output, exception",
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
                    "MAKE (n:NodeLabel)-[r:REL]->(n:NodeLabel);\n"
                    "FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);\n"
                    "CRITERIA p.name = 'Bar' or q.name = 'Bar';\n"
                    "REPORT wn(p), wn(q);"
                ),
                ["MAKE (n:NodeLabel)-[r:REL]->(n:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Multi Stage Query",
            ),
        ],
    )
    def test_extract_make_statement_from_query(
        self, sample_query: str, expected_output: list[str], exception
    ) -> None:

        with exception:
            test = extract_make_statement_from_query(sample_query)

            assert test == expected_output
