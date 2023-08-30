from ast import literal_eval
from re import split

from exceptions.wql.parsing import (
    ClauseSyntaxError,
    IllegalCharacterError,
    NonDirectedRelationshipError,
    ParamSyntaxError,
    RelationshipNameSyntaxError,
)
from models.wql import Clause
from wiggle_query_language.clauses.regexes.find.find_patterns import (
    FIND_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
)
from wiggle_query_language.clauses.regexes.make.make_patterns import (
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
)
from wiggle_query_language.clauses.regexes.patterns.properties import (
    CHECK_PROPERTIES_SYNTAX_REGEX,
    PROPERTIES_LIST_VALUE_REGEX,
)
from wiggle_query_language.clauses.regexes.patterns.relationships import (
    RELATIONSHIP_DIR_CHECK_REGEX,
)
from wiggle_query_language.clauses.regexes.patterns.utilities import ILLEGAL_CHARS_REGEX
from wiggle_query_language.clauses.regexes.report.report_patterns import (
    REPORT_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
)


def check_clause_spelling(query_string: str, clause: Clause) -> bool:
    """
    Checks the MAKE for a spelling mistake.
    :param query_string: The extracted MAKE statements.
    :param clause: The WQL clause.
    :return: True or raises and exception.
    """

    match clause:
        case Clause.MAKE:
            clause_syntax_regex = MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX
        case Clause.FIND:
            clause_syntax_regex = FIND_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX
        case clause.REPORT:
            clause_syntax_regex = REPORT_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX
        case _:
            raise Exception()

    if matches := clause_syntax_regex.findall(query_string):
        for match in matches:
            raise ClauseSyntaxError(
                message=f"SyntaxError: {match} was not recognised did you mean {clause.value}?"
            )

    return True


def check_property_syntax(params_string: str) -> bool:
    """
    Checks the formatting of the params string.
    :param params_string: The extracted MAKE statement
    :return: True or raises and exception.
    """

    exp_param_count = params_string.count(",") + 1
    colon_count = params_string.count(":")
    if exp_param_count != colon_count:
        raise ParamSyntaxError(message=f"SyntaxError: {params_string} missing : or ,")

    return True


def check_node_rel_properties(stmt_matches: list[str]) -> True:
    """
    Very crude check that the params match are up to snuff.
    :param stmt_matches: The extracted statements.
    :return: True or raises and exception.
    """

    for stmt in stmt_matches:
        if not (param_string := CHECK_PROPERTIES_SYNTAX_REGEX.findall(stmt)):
            continue

        for param_match_in in param_string:
            param_match = (
                param_match_in.replace("true", "True")
                .replace("false", "False")
                .replace("null", "None")
            )

            # remove the list from the params
            params_sans_list = PROPERTIES_LIST_VALUE_REGEX.sub("", param_match)
            check_property_syntax(params_sans_list)

            # check lists
            if params_lists := PROPERTIES_LIST_VALUE_REGEX.findall(param_match):
                for params_list in params_lists:
                    try:
                        literal_eval(params_list)
                    except SyntaxError:
                        raise ParamSyntaxError(
                            message=f"SyntaxError: {params_lists} missing a comma?"
                        )

    return True


def check_relationships(stmt_matches: list[str]) -> bool:
    """
    Checks to see that the created relationship is directed.
    :param stmt_matches: The extracted statements.
    :return: True or raises and exception.
    """

    for stmt in stmt_matches:
        if not (rels_matches := RELATIONSHIP_DIR_CHECK_REGEX.findall(stmt)):
            return True
        for rel in rels_matches:
            rel_pattern: str = rel[0]
            rel_name: str = rel[1]

            if "<" in rel_pattern and ">" in rel_pattern:
                raise NonDirectedRelationshipError(
                    message=f"Relationships must be unidirectional: {rel_pattern}"
                )
            if "<" not in rel_pattern and ">" not in rel_pattern:
                raise NonDirectedRelationshipError(
                    message=f"Relationships must be singly directed: {rel_pattern}"
                )

            if not rel_name.isupper() and rel_name:
                raise RelationshipNameSyntaxError(
                    f"Relationship names must be upper case: {rel_name} -> {rel_name.upper()}"
                )

            continue

    return True


def check_illegal_characters(stmt_matches: list[str]) -> bool:
    """
    Checks the MAKE/FIND statement does not contain ant illegal characters.
    :param stmt_matches: The extracted MAKE statements.
    :return: True or raises and exception.
    """
    for stmt in stmt_matches:
        if match := ILLEGAL_CHARS_REGEX.search(stmt):
            raise IllegalCharacterError(message=f"{match.group()} is not allowed")

    return True


def check_statement_syntax(stmt_matches: list[str]) -> bool:
    """
    Checks the syntax of the MAKE/FIND statement.
    :param stmt_matches: The extracted MAKE statements.
    :return: True or raises and exception.
    """

    for stmt in stmt_matches:
        stmt_split = split(r"[<>]+", stmt)

        for sub_stmt in stmt_split:
            # parens and curls must be even
            parens_count = sum(1 for x in sub_stmt if x in ("(", ")"))
            curly_count = sum(1 for x in sub_stmt if x in ("{", "}"))
            square_count = sum(1 for x in sub_stmt if x in ("[", "]"))

            if parens_count % 2 == 1:
                raise ClauseSyntaxError(
                    f"Node is missing a parentheses: ---> {sub_stmt} <---"
                )

            if curly_count % 2 == 1:
                raise ClauseSyntaxError(
                    f"Properties is missing a curly brace: ---> {sub_stmt} <---"
                )

            if square_count % 2 == 1:
                raise ClauseSyntaxError(
                    f"A Relationship or property list is missing a square bracket: ---> {sub_stmt} <---"
                )

    return True


def validate_statement(stmt_matches: list[str]) -> bool:
    """
    Handles the validation for the MAKE/FIND statement.
    :param stmt_matches: The extracted make statements.
    :return: True or raises and exception.
    """
    check_statement_syntax(stmt_matches)
    check_illegal_characters(stmt_matches)
    check_node_rel_properties(stmt_matches)
    check_relationships(stmt_matches)

    return True


if __name__ == "__main__":
    test_stmt_list = ["""MAKE (:NodeLabel)---[]--->(foo:NodeLabel);"""]

    a = [
        x.groupdict()
        for x in RELATIONSHIP_DIR_CHECK_REGEX.finditer(test_stmt_list[0])
        if x.group()
    ]
    b = RELATIONSHIP_DIR_CHECK_REGEX.findall(test_stmt_list[0])
    foo = check_relationships(test_stmt_list)
