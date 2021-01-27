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
            r.OPTIONAL_WHITESPACE.join([x.to_regex() for x in self.ast])
            + r.OPTIONAL_WHITESPACE
            + r.OPTIONAL_SEMICOLON
            + r.OPTIONAL_WHITESPACE
            + "$"
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
        # TODO Ensure matching quotes
        return r.NAME


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
        return "(\s+)".join([x.to_regex() for x in self.members])


@dataclass
class Choice(Group):
    def to_regex(self) -> str:
        return "(" + "|".join([x.to_regex() for x in self.members]) + ")"


@dataclass
class InParens(Group):
    def to_regex(self) -> str:
        return "\(" + "(\s+)".join([x.to_regex() for x in self.members]) + "\)"


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
        return "(" + str(self.wraps.to_regex()) + ")\s*(\s*,\s*" + str(self.wraps.to_regex()) + "+)*"


@dataclass
class Maybe(Modifier):
    def to_regex(self) -> str:
        return "(" + self.wraps.to_regex() + ")" + "?"
