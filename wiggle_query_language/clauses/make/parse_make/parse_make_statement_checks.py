from exceptions.wql.make import (
    MakeClauseSyntaxError,
    MakeParamSyntaxError,
    MakeNonDirectedRelationshipError,
    MakeIllegalCharacterError,
    MakeRelationshipNameSyntaxError,
)
from wiggle_query_language.clauses.regexes.make_patterns import (
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
    MAKE_STATEMENT_CHECK_PARAMS_SYNTAX_REGEX,
    RELATIONSHIP_DIR_CHECK_REGEX,
    PARAM_LIST_VALUE_REGEX,
    ILLEGAL_CHARS_REGEX,
)


def check_param_formatting(params_string: str) -> bool:
    """
    Checks the formatting of the params string.
    :param params_string: The extracted MAKE statement
    :return: True or raises and exception.
    """

    exp_param_count = params_string.count(",") + 1
    colon_count = params_string.count(":")
    if exp_param_count != colon_count:
        raise MakeParamSyntaxError(
            message=f"SyntaxError: {params_string} missing : or ,"
        )

    return True


def check_make_params(make_matches: list[str]) -> True:
    """
    Very crude check that the params match up with the colons
    :param make_matches:  The extracted MAKE statements.
    :return: True or raises and exception.
    """

    for stmt in make_matches:
        if not (param_string := MAKE_STATEMENT_CHECK_PARAMS_SYNTAX_REGEX.findall(stmt)):
            continue

        # TODO remove double loop, most of the time will be one match..
        for param_match_in in param_string:
            # TODO replace PARAM_LIST_VALUE_REGEX with ALL_PARAMS_KEY_VALUE_REGEX
            param_match = param_match_in.replace("true", "True").replace(
                "false", "False"
            )
            # remove the list from the params
            params_sans_list = PARAM_LIST_VALUE_REGEX.sub("", param_match)
            check_param_formatting(params_sans_list)

            # check list
            if params_lists := PARAM_LIST_VALUE_REGEX.findall(param_match):
                for params_list in params_lists:
                    try:
                        eval(params_list)
                    except SyntaxError:
                        raise MakeParamSyntaxError(
                            message=f"SyntaxError: {params_lists} missing a comma?"
                        )

    return True


def check_make_clause_syntax(query_string: str) -> bool:
    """
    Checks the syntax of the MAKE statement.
    :param query_string: The extracted MAKE statements.
    :return: True or raises and exception.
    """

    if matches := MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX.findall(query_string):
        for match in matches:
            raise MakeClauseSyntaxError(
                message=f"SyntaxError: {match} was not recognised did you mean MAKE?"
            )

    return True


def check_relationships(make_matches: list[str]) -> bool:
    """
    Checks to see that the created relationship is directed.
    :param make_matches: The extracted make statements.
    :return: True or raises and exception.
    """

    for stmt in make_matches:
        if not (rels_matches := RELATIONSHIP_DIR_CHECK_REGEX.findall(stmt)):
            return True
        for rel in rels_matches:
            rel_pattern: str = rel[0]
            rel_name: str = rel[1]

            if "<" in rel_pattern and ">" in rel_pattern:
                raise MakeNonDirectedRelationshipError(
                    message=f"Relationships must be unidirectional: {rel_pattern}"
                )
            if "<" not in rel_pattern and ">" not in rel_pattern:
                raise MakeNonDirectedRelationshipError(
                    message=f"Relationships must be singly directed: {rel_pattern}"
                )

            if not rel_name.isupper() and rel_name:
                raise MakeRelationshipNameSyntaxError(
                    f"Relationship names must be upper case: {rel_name} -> {rel_name.upper()}"
                )

            continue

    return True


def check_illegal_characters(make_matches: list[str]) -> bool:
    """
    Checks the MAKE statement does not contain ant illegal characters.
    :param make_matches: The extracted MAKE statements.
    :return: True or raises and exception.
    """
    for stmt in make_matches:
        if match := ILLEGAL_CHARS_REGEX.search(stmt):
            raise MakeIllegalCharacterError(message=f"{match.group()} is not allowed")

    return True


def validate_make_statement(make_matches: list[str]) -> bool:
    """
    Handles the validation for the make statement.
    :param make_matches: The extracted make statements.
    :return: True or raises and exception.
    """
    check_illegal_characters(make_matches)
    check_make_params(make_matches)
    check_relationships(make_matches)

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
