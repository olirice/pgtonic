############
# Concepts #
############


# public, perms, api_sch
_UNQUOTED_NAME = "([A-z_][A-z0-9_]*)"

# "api_V2", "sOmEaC"
_QUOTED_NAME = '("[^"]+?")'

###################
# Externally Used #
###################

SCHEMA_NAME = f"({_UNQUOTED_NAME}|{_QUOTED_NAME})"
ENTITY_NAME = f"({_UNQUOTED_NAME}|{_QUOTED_NAME})"

NAME = rf"({SCHEMA_NAME}\.{ENTITY_NAME}|{ENTITY_NAME})"

WHITESPACE = r"(\s+)"
OPTIONAL_WHITESPACE = r"(\s*)"

SEMICOLON = ";"
OPTIONAL_SEMICOLON = ";?"

START_OF_LINE = "^"
END_OF_LINE = "$"
