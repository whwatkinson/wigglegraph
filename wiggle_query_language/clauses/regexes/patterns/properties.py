from re import compile, IGNORECASE


# int: 1, float: 3.14, bool: true, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [...]
ALL_PROPERTIES_KEY_VALUE_REGEX = compile(
    (
        r"(?P<property_name>\w+)\s*:\s*(?P<property_value>(?P<none_type>null)|(?P<bool_type>true|false)|"
        r"(?P<float_type>\d+\.\d+)|(?P<int_type>[0-9]+)|(?P<list_type>\[[\w,\s'\"\.@\+]+\])|"
        r"(?P<string_type>[\w+\'\"@\.\s]+))"
    ),
    flags=IGNORECASE,
)
