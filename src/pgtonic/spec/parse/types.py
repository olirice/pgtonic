from dataclasses import dataclass
from typing import List, Optional, Dict, ClassVar

from pgtonic.spec import regex as r


class ToRegexMixin:
    def to_regex(self, where: Dict[str, str]) -> str:
        raise NotImplementedError()


@dataclass
class Base(ToRegexMixin):
    pass


##############
# Leaf Nodes #
##############


@dataclass
class Leaf(Base):
    content: str

    def to_regex(self, where: Dict[str, str]) -> str:
        # Is abstract, should never be in AST
        raise NotImplementedError()


@dataclass
class Literal(Leaf):
    def to_regex(self, where: Optional[Dict[str, str]]) -> str:
        return str(self.content)


@dataclass
class Argument(Leaf):
    """User input"""

    def to_regex(self, where: Dict[str, str]) -> str:
        return where[self.content]


@dataclass
class Pipe(Leaf):
    def to_regex(self, where: Dict[str, str]) -> str:
        # Should never be in AST
        raise NotImplementedError()


@dataclass
class UnqualifiedName(Leaf):
    def to_regex(self, where: Dict[str, str]) -> str:
        return r.UNQUALIFIED_NAME


@dataclass
class QualifiedName(Leaf):
    def to_regex(self, where: Dict[str, str]) -> str:
        return r.QUALIFIED_NAME


@dataclass
class Name(Leaf):
    def to_regex(self, where: Dict[str, str]) -> str:
        return r.NAME


###################
# Group Nodes
###################


@dataclass
class Group(Base):
    members: List[Base]

    def to_regex(self, where: Dict[str, str]) -> str:
        return join_w_whitespace(self.members, where)


@dataclass
class Choice(Group):
    def to_regex(self, where: Dict[str, str]) -> str:
        return "(" + "|".join([x.to_regex(where) for x in self.members]) + ")"


@dataclass
class InParens(Group):
    def to_regex(self, where: Dict[str, str]) -> str:
        return r"\(\s*" + r"\s+".join([x.to_regex(where) for x in self.members]) + r"\s*\)"


##################
# Modifier Nodes #
##################


@dataclass
class Modifier(Base):
    wraps: Base


@dataclass
class Repeat(Base):
    wraps: Base

    delimiter_regex: ClassVar[str]

    def to_regex(self, where: Dict[str, str]) -> str:
        self_reg = self.wraps.to_regex(where)
        return "(" + self_reg + r")(\s*" + self.delimiter_regex + r"\s*" + self_reg + r")*"


@dataclass
class RepeatComma(Repeat):
    """Comma separated"""

    delimiter_regex = ","


class RepeatOr(Repeat):
    """OR separated"""

    delimiter_regex = "OR"


class RepeatNone(Repeat):
    """Whitespace separated"""

    delimiter_regex = r"\w+"


@dataclass
class Maybe(Modifier):
    def to_regex(self, where: Dict[str, str]) -> str:
        return "(" + self.wraps.to_regex(where) + ")" + "?"


def resolves_to_maybe(node):
    """Does the node unwrap to a Maybe"""
    if isinstance(node, Maybe):
        return True
    elif isinstance(node, Group):
        return resolves_to_maybe(node.members[0])
    elif isinstance(node, Modifier):
        return resolves_to_maybe(node.wraps)
    return False


def join_w_whitespace(nodes: List[Base], where: Dict[str, str]) -> str:
    """Join nodes, respecting modifiers"""
    output = []

    for ix, node in enumerate(nodes):

        # Maybes handle their own whitespace
        if resolves_to_maybe(node):  # and not ix + 1 == len(nodes):
            output.append(r.OPTIONAL_WHITESPACE + node.to_regex(where) + r.OPTIONAL_WHITESPACE)
        else:
            if ix != 0:
                if not resolves_to_maybe(nodes[ix - 1]):
                    output.append(r.WHITESPACE)
            output.append(node.to_regex(where))

    return "".join(output)
