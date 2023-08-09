from typing import Optional

from exceptions.wql.make import (
    MakeClauseSyntaxError,
    MakeParamSyntaxError,
    MakeNonDirectedRelationshipError,
)
from models.wql.parsed_query import ParsedMake
from wiggle_query_language.clauses.regexes.make import (
    MAKE_STATEMENT_ALL,
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX,
    MAKE_STATEMENT_CHECK_PARAMS_SYNTAX,
    NODES_RELS_PATTERN,
    RELATIONSHIP_DIR_CHECK,
    PARAM_LIST_VALUE,
)


def check_param_formatting(params_string: str) -> bool:
    """
    Chesk the
    :param params_string:
    :return:
    """

    exp_param_count = params_string.count(",") + 1
    colon_count = params_string.count(":")
    if exp_param_count != colon_count:
        raise MakeParamSyntaxError(f"SyntaxError: {params_string} missing : or ,")

    return True


def check_make_params(make_matches: list[str]) -> True:
    """
    Very crude check that the params match up with the colons
    :param make_matches:  The extracted MAKE statements.
    :return: A bool for testing.
    """

    for stmt in make_matches:
        if not (param_string := MAKE_STATEMENT_CHECK_PARAMS_SYNTAX.findall(stmt)):
            continue

        # TODO remove double loop, most of the time will be one match..
        for param_match in param_string:
            # remove the list from the params
            params_sans_list = PARAM_LIST_VALUE.sub("", param_match)
            check_param_formatting(params_sans_list)

            # check list
            if params_lists := PARAM_LIST_VALUE.findall(param_match):
                for params_list in params_lists:
                    try:
                        # TODO remove this..
                        eval(params_list)
                    except SyntaxError:
                        raise MakeParamSyntaxError(
                            f"SyntaxError: {params_lists} missing a comma?"
                        )

    return True


def check_make_clause_syntax(query_string: str) -> None:
    """
    Checks the syntax of the MAKE statement.
    :param query_string: The extracted MAKE statements.
    :return: None or an Exception
    """

    if matches := MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX.findall(query_string):
        for match in matches:
            raise MakeClauseSyntaxError(
                f"SyntaxError: {match} was not recognised did you mean MAKE?"
            )

    return None


def extract_all_make_statements(query_string: str) -> Optional[list[str]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """

    if make_matches := [x.group() for x in MAKE_STATEMENT_ALL.finditer(query_string)]:
        return make_matches

    check_make_clause_syntax(query_string)

    return None


def build_parsed_make(statement: str) -> ParsedMake:
    """
    Handles building of the ParsedMake.
    :param statement: The raw make statement.
    :return: A ParsedMake Object.
    """
    parsed_pattern_dict = [
        x.groupdict() for x in NODES_RELS_PATTERN.finditer(statement) if x.group()
    ]

    parsed_make = ParsedMake(
        raw_statement=statement, parsed_pattern_list=parsed_pattern_dict
    )

    return parsed_make


def check_relationships(make_matches: list[str]) -> bool:
    """
    Checks to see that the created relationship is directed.
    :param make_matches: The extracted make statements.
    :return: A bool for testing.
    """

    for stmt in make_matches:
        rels = RELATIONSHIP_DIR_CHECK.findall(stmt)

        for rel in rels:
            if "<" in rel and ">" in rel:
                raise MakeNonDirectedRelationshipError(
                    "Relationships must be unidirectional"
                )
            if "<" not in rel and ">" not in rel:
                raise MakeNonDirectedRelationshipError(
                    "Relationships must be singly directed"
                )

            continue

    return True


def check_illegal_characters(make_matches: list[str]) -> bool:
    pass


def validate_make_statement(make_matches: list[str]) -> bool:
    """
    Handles the validation for the make statement
    :param make_matches: The extracted make statements
    :return: The
    """
    check_illegal_characters(make_matches)
    check_make_params(make_matches)
    check_relationships(make_matches)

    return True


def parse_make_statement_from_query_string(
    query_string: str,
) -> Optional[list[ParsedMake]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """
    make_matches = extract_all_make_statements(query_string)
    if not validate_make_statement(make_matches):
        raise Exception("make_matches says no")

    if make_matches:
        return [build_parsed_make(statement=stmt) for stmt in make_matches]
    else:
        return None


if __name__ == "__main__":
    qs = """"MAKE (left_node_handle:LeftNodeLabel { int: 1   , str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]});"""
    s = parse_make_statement_from_query_string(qs)
    a = 1
