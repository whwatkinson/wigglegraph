def relationship_name_is_in_index(
    relationship_name_set: set[str], relationship_name_index: set[str]
) -> bool:
    return bool(relationship_name_set.intersection(relationship_name_index))
