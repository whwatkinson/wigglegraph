from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes import EXTRA_ALLOWED_CHARS

# int: 1, float: 3.14, bool: true, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [...]
ALL_PROPERTIES_KEY_VALUE_REGEX = compile(
    pattern=(
        r"(?P<property_name>\w+)\s*:\s*(?P<property_value>(?P<none_type>null)|(?P<bool_type>true|false)|"
        r"(?P<float_type>\d+\.\d+)|(?P<int_type>[0-9]+)|(?P<list_type>\[[\w,\s'\"\.@\+]+\])|"
        r"(?P<string_type>[\w+\'\"@\.\s]+))"
    ),
    flags=IGNORECASE,
)


# {first_name:'Harry' , last_name:'Watkinson' , favourite_number: 6 , favourite_color: 'green'}
CHECK_PROPERTIES_SYNTAX_REGEX = compile(
    pattern=rf"(?P<all_props>{{[\w:\s,'\"\.\[\]{EXTRA_ALLOWED_CHARS}]+}})",
    flags=IGNORECASE,
)


# [1, '2', "2_4", "3 4", 3.14]
PROPERTIES_LIST_VALUE_REGEX = compile(
    pattern=rf"(?P<list_value>\[[\w,\s'\"\.{EXTRA_ALLOWED_CHARS}]+])", flags=IGNORECASE
)
