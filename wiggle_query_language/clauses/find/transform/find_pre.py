from models.wql import ParsedFind, MakePre, Clause

# from wiggle_query_language.clauses.parsing_helpers.parse_properties import (
#     get_property_dict,
# )


def process_parsed_find_list(parsed_find_list: list[ParsedFind]):
    for parsed_find in parsed_find_list:
        if parsed_find.clause is not Clause.FIND:
            raise Exception(f"Expecting FIND but got {parsed_find.clause}")

        for parsed_pattern in parsed_find.parsed_pattern_list:
            MakePre()

            # FOR ONE NODE
            # left_handle = parsed_pattern.left_node_handle
            # node_label = parsed_pattern.left_node_label
            # left_props = get_property_dict(parsed_pattern.left_node_props)
            #
            # a = 1


if __name__ == "__main__":
    from wiggle_query_language.clauses.find.parse_find.parse_find_statement import (
        parse_find_statement_from_query_string,
    )

    # Just doing Onde node for now then will build it up...
    query_string = """"FIND (left_node_handle:LeftNodeLabel { int: 1, str: '2', str2:"2_4", float: 3.14, list: [ 1, '2', "2_4", "3 4", 3.14, true, false, null ]});"""
    finds = parse_find_statement_from_query_string(query_string)

    process_parsed_find_list(finds)

    a = 1
