from dataclasses import dataclass
from typing import List

from pgtonic.spec import regex as r


class ToRegexMixin:
    def to_regex(self) -> str:
        raise NotImplementedError()


@dataclass
class Base(ToRegexMixin):
    pass


@dataclass
class Spec(ToRegexMixin):
    """Represents a postgres specification template

    e.g.

        CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] VIEW name [ ( column_name [, ...] ) ]
        [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
        AS query

    """

    ast: List[Base]

    def to_regex(self) -> str:
        return (
            join_w_whitespace(self.ast)
            + r.OPTIONAL_WHITESPACE
            + r.OPTIONAL_SEMICOLON
            + r.OPTIONAL_WHITESPACE
            + r.END_OF_LINE
        )


##############
# Leaf Nodes #
##############


@dataclass
class Leaf(Base):
    content: str

    def to_regex(self) -> str:
        # Is abstract, should never be in AST
        raise NotImplementedError()


@dataclass
class Literal(Leaf):
    def to_regex(self) -> str:
        return str(self.content)


@dataclass
class Argument(Leaf):
    """User input"""

    def to_regex(self) -> str:
        if self.content in ("table_name", "function_name", "sequence_name"):
            return r.NAME
        elif self.content in ("schema_name", "table_namespace", "tablespace_name"):
            return r.SCHEMA_NAME
        elif self.content in (
            "column",
            "role_name",
            "database_name",
            "fdw_name",
            "server_name",
            "arg_name",
            "lang_name",
        ):
            return r.ENTITY_NAME
        elif self.content == "arg_type":
            return ".+"
        elif self.content == "argmode":
            # https://www.postgresql.org/docs/13/sql-createfunction.html
            return "IN|OUT|INOUT"
        elif self.content == "loid":
            # large object id
            return r"\d+"
        elif self.content == "role_specification":
            # https://www.postgresql.org/docs/13/sql-grant.html
            return f"PUBLIC|CURRENT_USER|SESSION_USER|(GROUP{r.OPTIONAL_WHITESPACE})?{r.ENTITY_NAME}"
        else:
            raise Exception(f"unknown arg name {self.content}")


@dataclass
class Pipe(Leaf):
    def to_regex(self) -> str:
        # Should never be in AST
        raise NotImplementedError()


###################
# Group Nodes
###################


@dataclass
class Group(Base):
    members: List[Base]

    def to_regex(self) -> str:
        return join_w_whitespace(self.members)


@dataclass
class Choice(Group):
    def to_regex(self) -> str:
        return "(" + "|".join([x.to_regex() for x in self.members]) + ")"


@dataclass
class InParens(Group):
    def to_regex(self) -> str:
        return r"\(\s*" + r"\s+".join([x.to_regex() for x in self.members]) + r"\s*\)"


##################
# Modifier Nodes #
##################


@dataclass
class Modifier(Base):
    wraps: Base


@dataclass
class Repeat(Modifier):
    """Comma separated"""

    def to_regex(self) -> str:
        return "(" + str(self.wraps.to_regex()) + r")\s*(\s*,\s*(" + str(self.wraps.to_regex()) + ")+)*"


@dataclass
class Maybe(Modifier):
    def to_regex(self) -> str:
        return "(" + self.wraps.to_regex() + r"\s*)" + "?"


def join_w_whitespace(nodes: List[Base]) -> str:
    output = []

    for ix, node in enumerate(nodes):
        output.append(node.to_regex())
        if not isinstance(node, Maybe) and not ix + 1 == len(nodes):
            output.append(r.WHITESPACE)
    return "".join(output)
