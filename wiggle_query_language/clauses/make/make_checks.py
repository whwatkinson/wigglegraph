from exceptions.wql.make import (
    MakeClauseSyntaxError,
    MakeParamSyntaxError,
    MakeNonDirectedRelationshipError,
    MakeIllegalCharacterError,
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
        for param_match in param_string:
            # remove the list from the params
            params_sans_list = PARAM_LIST_VALUE_REGEX.sub("", param_match)
            check_param_formatting(params_sans_list)

            # check list
            if params_lists := PARAM_LIST_VALUE_REGEX.findall(param_match):
                for params_list in params_lists:
                    try:
                        # TODO remove this..
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
        rels = RELATIONSHIP_DIR_CHECK_REGEX.findall(stmt)
        # TODO ENFORCE UPPER CASE RELLABEL
        for rel in rels:
            if "<" in rel and ">" in rel:
                raise MakeNonDirectedRelationshipError(
                    message="Relationships must be unidirectional"
                )
            if "<" not in rel and ">" not in rel:
                raise MakeNonDirectedRelationshipError(
                    message="Relationships must be singly directed"
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
