from exceptions.wql.parsing import NonDirectedRelationshipError


def relationship_is_left_to_right(parsed_relationship_pattern: str) -> bool:
    """
    Checks the direction of the relationship.
    :param parsed_relationship_pattern: The extracted relationship expression.
    :return: Ture if LTR, False if RTL.
    """
    if "<" in parsed_relationship_pattern and ">" in parsed_relationship_pattern:
        raise NonDirectedRelationshipError(
            f"Non directed relationship found: {parsed_relationship_pattern}"
        )

    return True if parsed_relationship_pattern[-1] == ">" else False
