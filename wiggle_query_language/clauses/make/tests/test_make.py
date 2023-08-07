from contextlib import contextmanager
from typing import Generator

import pytest

from exceptions.wql.make import MakeClauseSyntaxError, MakeParamSyntaxError
from wiggle_query_language.clauses.make.make import (
    extract_all_make_statements,
    check_make_clause_syntax,
    check_make_params,
)


@contextmanager
def does_not_raise() -> Generator:
    yield None


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

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_query, expected_output, exception",
        [
            pytest.param(
                "MAKE (:NodeLabel)-[:]->(:NodeLabel), (:NodeLabel2)-[:]->(:NodeLabel2);",
                [
                    "MAKE (:NodeLabel)-[:]->(:NodeLabel), (:NodeLabel2)-[:]->(:NodeLabel2);"
                ],
                does_not_raise(),
                id="EXP PASS: Simple Case",
            ),
        ],
    )
    def test_extract_all_make_statements__more_pattern_matching(
        self, test_query: str, expected_output: list[str], exception
    ) -> None:

        with exception:
            test = extract_all_make_statements(test_query)
            assert test == expected_output

    @pytest.mark.parametrize(
        "test_make_stmt, expected_value, exception",
        [
            pytest.param(
                "MAKeeE (node:NodeLabel);]",
                None,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "MAk (node:NodeLabel);",
                None,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "Mkea (node:NodeLabel);",
                None,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "MAKeeE (node:NodeLabel);",
                None,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "JSLW (node:NodeLabel);",
                None,
                pytest.raises(MakeClauseSyntaxError),
                id="EXP EXEC",
            ),
        ],
    )
    def test_check_make_syntax(
        self, test_make_stmt: str, expected_value: None, exception
    ) -> None:

        with exception:
            check_make_clause_syntax(test_make_stmt)

    @pytest.mark.parametrize(
        "test_make_stmt, expected_value, exception",
        [
            pytest.param(
                ["MAKE (n:Person);"], None, does_not_raise(), id="EXP PASS: No params"
            ),
            pytest.param(
                ["MAKE (n:Person{first_name:'Harry'});"],
                None,
                does_not_raise(),
                id="EXP PASS: One params",
            ),
            pytest.param(
                ["MAKE (n:Person{first_name:'Harry', last_name:'Watkinson'});"],
                None,
                does_not_raise(),
                id="EXP PASS: 1 comma",
            ),
            pytest.param(
                [
                    """MAKE (:NodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})-[r:REL{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(foo:NodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]} );"""
                ],
                None,
                pytest.raises(MakeParamSyntaxError),
                id="EXP PASS: 1 comma",
            ),
        ],
    )
    def test_check_make_params(
        self, test_make_stmt: list[str], expected_value: None, exception
    ) -> None:
        with exception:
            check_make_params(test_make_stmt)
