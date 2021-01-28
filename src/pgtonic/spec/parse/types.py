from dataclasses import dataclass
from typing import ClassVar, Dict, List

from pgtonic.spec import regex as r


class ToRegexMixin:
    def to_regex(self, where: Dict[str, List["Base"]]) -> str:
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

    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        # Is abstract, should never be in AST
        raise NotImplementedError()


@dataclass
class Literal(Leaf):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        return str(self.content)


@dataclass
class Argument(Leaf):
    """User input"""

    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        ast = where[self.content]

        if len(ast) == 1:
            return ast[0].to_regex(where={})
        return Group(ast).to_regex(where={})


@dataclass
class Pipe(Leaf):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        # Should never be in AST
        raise NotImplementedError()


@dataclass
class UnqualifiedName(Leaf):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        return r.UNQUALIFIED_NAME


@dataclass
class QualifiedName(Leaf):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        return r.QUALIFIED_NAME


@dataclass
class Name(Leaf):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        return r.NAME


###################
# Group Nodes
###################


@dataclass
class Group(Base):
    members: List[Base]

    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        return apply_whitespace(self.members, where)


@dataclass
class Choice(Group):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        return "(" + "|".join([x.to_regex(where) for x in self.members]) + ")"


@dataclass
class InParens(Group):
    def to_regex(self, where: Dict[str, List[Base]]) -> str:
        # return r"\(\s*" + r"\s+".join([x.to_regex(where) for x in self.members]) + r"\s*\)"
        return r"\(\s*" + apply_whitespace(self.members, where) + r"\s*\)"


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

    def to_regex(self, where: Dict[str, List[Base]]) -> str:
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
    def to_regex(self, where: Dict[str, List[Base]], leading_ws: bool, trailing_ws: bool) -> str:  # type: ignore
        return (
            "("
            + (r.WHITESPACE if leading_ws else "")
            + self.wraps.to_regex(where)
            + (r.WHITESPACE if trailing_ws else "")
            + ")?"
        )


def apply_whitespace(nodes: List[Base], where: Dict[str, List[Base]]) -> str:
    """Join nodes, respecting modifiers"""
    output = []

    # OTHER OTHER
    # OTHER MAYBE
    # MA
    # MAYBE MAYBE

    from flupy import flu

    node_iter = flu([None] + nodes[:-1]).zip_longest(nodes, nodes[1:]).collect()  # type: ignore

    for ix, (previous, current, next_) in enumerate(node_iter):

        if isinstance(current, Maybe):

            if previous is None:
                leading_ws = False
            elif isinstance(previous, Maybe):
                leading_ws = False
            elif isinstance(previous, Repeat):
                leading_ws = True
            else:
                leading_ws = False

            if next_ is None:
                trailing_ws = False
            elif isinstance(next_, Maybe):
                trailing_ws = True
            elif isinstance(next_, Repeat):
                trailing_ws = True
            else:
                trailing_ws = True

            output.append(current.to_regex(where, trailing_ws=trailing_ws, leading_ws=leading_ws))
            continue

        elif previous is None:
            output.append(current.to_regex(where))
            continue

        elif isinstance(previous, Maybe):
            output.append(current.to_regex(where))
            continue

        output.append(r.WHITESPACE)
        output.append(current.to_regex(where))

    return "".join(output)
