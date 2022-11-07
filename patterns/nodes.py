from re import compile

# MAKE (n:Node) -> MAKE
make_clause_regex = compile(r"""(?P<clause>MAKE|make)""")

# MAKE (n:Node) -> n
node_handle_regex = compile(r"""\(\s*(?P<handle>\w+)\s*:""")

# MAKE (n:Node) -> Node
node_label_regex = compile(r"""\(\s*\w*\s*:\s*(?P<node_label>\w+)""")

# MAKE (n:Node) -> (n:Node)
nodes_regex = compile(r"""(?P<node>\(\s*\w*\s*:[\w\'\":|\s\-.,\[\]{}]+\))""")


# MAKE (n:Node{foo: "bar"}) -> foo: "bar"
node_params_regex = compile(r"""\s*?(?P<params>[\w\':|\s\-.,\[\]]+)?\s*}\s*\)""")

# foo: "bar", "foo: 3.14159" -> 'foo: "bar"'
key_value_regex = compile(r"""(?P<key>\w+):\s?(?P<value>[\[\]\s,'\w\-.]+)""")

relationship_regex = compile(
    r"""(?P<node1>\(.*:.+\))(?P<rel><*-\[.*:.+]->*)(?P<node2>\(.*:.+\))"""
)
