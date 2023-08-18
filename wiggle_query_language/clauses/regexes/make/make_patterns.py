from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes import ILLEGAL_CHARS

# MAKE *;
MAKE_STATEMENT_ALL_REGEX = compile(
    r"(?P<make_stmt_all>MAKE\s*\(.+\);)", flags=IGNORECASE
)


# AKME (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX = compile(
    (
        r"\s?(?P<make_syntax_error>maek|mkae|mkea|meak|meka|amke|amek|akme"
        r"|akem|aemk|aekm|kmae|kmea|kame|kaem|kema|keam|emak|emka|eamk|eakm|ekma|ekam)\s?\("
    ),
    flags=IGNORECASE,
)

# #%&*
ILLEGAL_CHARS_REGEX = compile(rf"[{ILLEGAL_CHARS}]", flags=IGNORECASE)
