import pytest

from exceptions.wql.parsing import (
    ClauseSyntaxError,
    IllegalCharacterError,
    NonDirectedRelationshipError,
    ParamSyntaxError,
    RelationshipNameSyntaxError,
)

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_statement_checks import (
    check_illegal_characters,
    check_make_clause_spelling,
    check_node_rel_properties,
    check_relationships,
    check_statement_syntax,
)

# TODO move and separate the test


class TestWqlMake:
    @pytest.mark.parametrize(
        "test_make_stmt, exception",
        [
            pytest.param(
                "MAEK (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "eMAk (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "EMka (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "KMAe (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "EKAM (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
        ],
    )
    def test_check_make_clause_spelling(self, test_make_stmt: str, exception) -> None:
        with exception:
            test = check_make_clause_spelling(test_make_stmt)
            assert test is True

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
                    """MAKE (n:Person{first_name:'Harry', last_name:'Watkinson', bool: true, list: [1, '2', "2_4", "3 4", 3.14]});"""
                ],
                does_not_raise(),
                id="EXP PASS: 1 comma",
            ),
            pytest.param(
                [
                    """MAKE (:NodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4" 3.14]});"""
                ],
                pytest.raises(ParamSyntaxError),
                id="EXP EXEC: Missing comma in param list",
            ),
        ],
    )
    def test_check_node_rel_properties(
        self, test_make_stmt: list[str], exception
    ) -> None:
        with exception:
            test = check_node_rel_properties(test_make_stmt)
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
                pytest.raises(NonDirectedRelationshipError),
                id="EXP EXEC: Non directed single relationship",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[]-(:NodeLabel);"],
                pytest.raises(NonDirectedRelationshipError),
                id="EXP EXEC: Non directed single relationship, no colon",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)<-[:]->(:NodeLabel);"],
                pytest.raises(NonDirectedRelationshipError),
                id="EXP EXEC: Rel is pointing both ways",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:]->(:NodeLabel)-[:]-(:NodeLabel);"],
                pytest.raises(NonDirectedRelationshipError),
                id="EXP EXEC: Triple node with two relationships, one not directed",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)-[:rel]->(:NodeLabel);"],
                pytest.raises(RelationshipNameSyntaxError),
                id="EXP EXEC: lowercase rel name",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)--[:rel]-->(:NodeLabel);"],
                pytest.raises(RelationshipNameSyntaxError),
                id="EXP EXEC: Double node with long relationship, lowercase rel name",
            ),
            pytest.param(
                ["MAKE (:NodeLabel)--[:rel]-->(:NodeLabel);"],
                pytest.raises(RelationshipNameSyntaxError),
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
                pytest.raises(IllegalCharacterError),
                id="EXP EXEC: Illegal char *",
            ),
            pytest.param(
                ["MAKE (:NodeLabel#);"],
                pytest.raises(IllegalCharacterError),
                id="EXP EXEC: Illegal char #",
            ),
            pytest.param(
                ["""MAKE (:NodeLabel{ int: 1 , str: '2', st%r2:"2_4"});"""],
                pytest.raises(IllegalCharacterError),
                id="EXP EXEC: Illegal char %",
            ),
            pytest.param(
                [
                    """MAKE (left_node_handle:LeftNodeLabel{int: 1}) -[:]-> (middle_node_label:&MiddleNodeLabel) -[:]->(right_node_label:RightNodeLabel);"""
                ],
                pytest.raises(IllegalCharacterError),
                id="EXP EXEC: Illegal char &",
            ),
            pytest.param(
                ["""MAKE (:NodeLabel{ int: 1 , str: '$2', str2:"2_4"});"""],
                pytest.raises(IllegalCharacterError),
                id="EXP EXEC: Illegal char $",
            ),
        ],
    )
    def test_check_illegal_characters(
        self, test_make_matches: list[str], exception
    ) -> None:
        with exception:
            test = check_illegal_characters(test_make_matches)
            assert test is True

    @pytest.mark.parametrize(
        "test_make_matches, exception",
        [
            pytest.param(
                ["MAKE (:NodeLabel);"],
                does_not_raise(),
                id="EXP PASS: No syntax error",
            ),
            pytest.param(
                ["MAKE (:NodeLabel;"],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing ( on on Node",
            ),
            pytest.param(
                ["MAKE (:NodeLabel;"],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing ) on Node",
            ),
            pytest.param(
                ["""MAKE (:NodeLabel{ int: 1 , str: '$2', str2:"2_4"};"""],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing ) on Node with props",
            ),
            pytest.param(
                ["""MAKE (:NodeLabel{ int: 1 , str: '$2', str2:"2_4");"""],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing } on Node with props",
            ),
            pytest.param(
                [
                    """MAKE (:NodeLabel{str: '2'})-[]->(:NodeLabel{str2:"2_4"})-[rel2:REL2{float: 3.14}]->:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]});"""
                ],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing ( on right Node",
            ),
            pytest.param(
                [
                    """MAKE (:NodeLabel{str: '2'})-[->(:NodeLabel{str2:"2_4"})-[rel2:REL2{float: 3.14}]->:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]});"""
                ],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing [ on left rel",
            ),
            pytest.param(
                [
                    """MAKE (:NodeLabel{str: '2'})-[]->(:NodeLabel{str2:"2_4"})-[rel2:REL2{float: 3.14}]->:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14});"""
                ],
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC: Missing [ on right node list",
            ),
        ],
    )
    def test_check_statement_syntax(self, test_make_matches: list[str], exception):
        with exception:
            test = check_statement_syntax(test_make_matches)
            assert test is True
