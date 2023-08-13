import pytest

from exceptions.wql.make import (
    MakeClauseSyntaxError,
    MakeParamSyntaxError,
    MakeNonDirectedRelationshipError,
    MakeIllegalCharacterError,
    MakeRelationshipNameSyntaxError,
)
from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_statement_checks import (
    check_make_clause_syntax,
    check_make_params,
    check_relationships,
    check_illegal_characters,
)


class TestWqlMake:
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

    # @pytest.mark.xfail()
    @pytest.mark.parametrize(
        "test_make_stmt, exception",
        [
            pytest.param(
                ["MAKE (n:Person);"], does_not_raise(), id="EXP PASS: No params"
            ),
            pytest.param(
                ["MAKE (n:Person{first_name:'Harry'});"],
                does_not_raise(),
                id="EXP PASS: One params",
            ),
            pytest.param(
                [
                    """MAKE (n:Person{first_name:'Harry', last_name:'Watkinson', list: [1, '2', "2_4", "3 4", 3.14]});"""
                ],
                does_not_raise(),
                id="EXP PASS: 1 comma",
            ),
            pytest.param(
                [
                    """MAKE (:NodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4" 3.14]});"""
                ],
                pytest.raises(MakeParamSyntaxError),
                id="EXP EXEC: Missing comma in param list",
            ),
        ],
    )
    def test_check_make_params(self, test_make_stmt: list[str], exception) -> None:
        with exception:
            test = check_make_params(test_make_stmt)
            assert test is True

    @pytest.mark.parametrize(
        "test_make_matches, exception",
        [
            pytest.param(
                ["MAKE (:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: No relationship",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:]->(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Double node with one relationship",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:]->(:NodeLabel)-[:]->(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Triple node with two relationships, ltr",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:]->(:NodeLabel)<-[:]-(:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: Triple node with two relationships, both pointing to middle",
            ),
            pytest.param(
                [
                    """"MAKE (:NodeLabel{int: 1})-[rel1:REL{str: '2'}]->(:NodeLabel{str2:"2_4"})<-[rel2:REL2{float: 3.14}]-(:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]}});"""
                ],
                does_not_raise(),
                id="EXP EXEC: Triple node with two relationships ltr and rtl.",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:]-(:NodeLabel);"],
                pytest.raises(MakeNonDirectedRelationshipError),
                id="EXP EXEC: Non directed single relationship",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[]-(:NodeLabel);"],
                pytest.raises(MakeNonDirectedRelationshipError),
                id="EXP EXEC: Non directed single relationship, no colon",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)<-[:]->(:NodeLabel);"],
                pytest.raises(MakeNonDirectedRelationshipError),
                id="EXP EXEC: Rel is pointing both ways",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:]->(:NodeLabel)-[:]-(:NodeLabel);"],
                pytest.raises(MakeNonDirectedRelationshipError),
                id="EXP EXEC: Triple node with two relationships, one not directed",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:rel]->(:NodeLabel);"],
                pytest.raises(MakeRelationshipNameSyntaxError),
                id="EXP EXEC: lowercase rel name",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)--[:rel]-->(:NodeLabel);"],
                pytest.raises(MakeRelationshipNameSyntaxError),
                id="EXP EXEC: Double node with long relationship, lowercase rel name",
            ),
        ],
    )
    def test_check_relationship(self, test_make_matches: list[str], exception) -> None:
        with exception:
            test = check_relationships(test_make_matches)
            assert test is True

    @pytest.mark.parametrize(
        "test_make_matches, exception",
        [
            pytest.param(
                ["MAKE (:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: No relationship",
            ),
            pytest.param(
                ["MAKE (:NodeLabel*);"],
                pytest.raises(MakeIllegalCharacterError),
                id="EXP EXEC: Illegal char *",
            ),
            pytest.param(
                ["MAKE (:NodeLabel#);"],
                pytest.raises(MakeIllegalCharacterError),
                id="EXP EXEC: Illegal char #",
            ),
            pytest.param(
                ["""MAKE (:NodeLabel{ int: 1 , str: '2', st%r2:"2_4"});"""],
                pytest.raises(MakeIllegalCharacterError),
                id="EXP EXEC: Illegal char %",
            ),
            pytest.param(
                [
                    """MAKE (left_node_handle:LeftNodeLabel{int: 1}) -[:]-> (middle_node_label:&MiddleNodeLabel) -[:]->(right_node_label:RightNodeLabel);"""
                ],
                pytest.raises(MakeIllegalCharacterError),
                id="EXP EXEC: Illegal char &",
            ),
            pytest.param(
                ["""MAKE (:NodeLabel{ int: 1 , str: '$2', str2:"2_4"});"""],
                pytest.raises(MakeIllegalCharacterError),
                id="EXP EXEC: Illegal char $",
            ),
        ],
    )
    def test_check_illegal_characters(
        self, test_make_matches: list[str], exception
    ) -> None:
        with exception:
            check_illegal_characters(test_make_matches)
            assert True
