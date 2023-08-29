from itertools import permutations


def get_clause_all_regex(clause: str) -> str:
    """
    Gets the $CLAUSE all regex.
    :param clause: The WQL clause.
    :return: A regex expression.
    """
    return rf"(?P<clause_stmt_all>({clause.upper()}|{clause.lower()})\s*\(.+\);)"


def get_clause_permutations(clause: str) -> str:
    """
    Gets the $CLAUSE regex for checking for a spelling mistake.
    :param clause: The WQL clause.
    :return: A string of the permutations.
    """
    all_permutations_joined = "|".join(["".join(x) for x in permutations(clause)])
    return all_permutations_joined


def get_clause_permutations_regex(clause: str) -> str:
    """
    Gets the $CLAUSE regex for checking for a spelling mistake.
    :param clause: The WQL clause.
    :return: A regex expression.
    """
    all_permutations_joined = get_clause_permutations(clause)

    clause_permutations_regex = (
        rf"\s?(?P<clause_syntax_error>{all_permutations_joined})\s?\("
    )

    return clause_permutations_regex
