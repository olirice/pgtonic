############
# Concepts #
############


# TODO: Exclude SQL keywords when unquoted. e.g. "TABLE"
# public, perms, api_sch
_UNQUOTED_NAME = "([A-z_][A-z0-9_]*)"
# "api_V2", "sOmEaC"
_QUOTED_NAME = '("[^"]+?")'

# For making regex more readable while debugging
# _UNQUOTED_NAME = r"\w+"
# _QUOTED_NAME = r'[\w"]+'

###################
# Externally Used #
###################

SCHEMA_NAME = f"({_UNQUOTED_NAME}|{_QUOTED_NAME})"
ENTITY_NAME = f"({_UNQUOTED_NAME}|{_QUOTED_NAME})"

QUALIFIED_NAME = rf"({SCHEMA_NAME}\.{ENTITY_NAME})"
UNQUALIFIED_NAME = rf"({ENTITY_NAME})"
NAME = rf"({QUALIFIED_NAME}|{UNQUALIFIED_NAME})"

WHITESPACE = r"(\s+)"
OPTIONAL_WHITESPACE = r"(\s*)"

SEMICOLON = ";"
OPTIONAL_SEMICOLON = ";?"

START_OF_LINE = "^"
END_OF_LINE = "$"
