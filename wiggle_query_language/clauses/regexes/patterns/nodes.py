from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes.patterns.patterns_helpers import (
    get_node_pattern_regex,
)

# (NodeHandle: NodeLabel {NodeProps})
NODE_HANDLE_LABEL_PARAMS_REGEX = compile(
    pattern=rf"{get_node_pattern_regex('this')}", flags=IGNORECASE
)
