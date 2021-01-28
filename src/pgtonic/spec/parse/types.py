from dataclasses import dataclass
from typing import List, Optional, Dict, ClassVar, Type

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
        ast = where[self.content]

        if len(ast) == 1:
            return ast[0].to_regex(where={})
        return Group(ast).to_regex(where={})


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
        return apply_whitespace(self.members, where)


@dataclass
class Choice(Group):
    def to_regex(self, where: Dict[str, str]) -> str:
        return "(" + "|".join([x.to_regex(where) for x in self.members]) + ")"


@dataclass
class InParens(Group):
    def to_regex(self, where: Dict[str, str]) -> str:
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
    def to_regex(self, where: Dict[str, str], leading_ws: bool = False, trailing_ws: bool = True) -> str:
        return (
                "(" 
                + (r.WHITESPACE if leading_ws else '')
                + self.wraps.to_regex(where)
                + (r.WHITESPACE if trailing_ws else '')
                + ")?"
        )


def resolves_to(node, type_: Type):
    """Does the node unwrap to a *type_*"""
    if isinstance(node, type_):
        return True
    elif isinstance(node, Group):
        return resolves_to(node.members[0], type_)
    elif isinstance(node, Modifier):
        return resolves_to(node.wraps, type_)
    return False


def apply_whitespace(nodes: List[Base], where: Dict[str, str], is_top=False) -> str:
    """Join nodes, respecting modifiers"""
    output = []

    # OTHER OTHER
    # OTHER MAYBE
    # MA
    # MAYBE MAYBE

    from flupy import flu

    node_iter = flu([None] + nodes[:-1]).zip_longest(nodes, nodes[1:]).collect() # type: ignore

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
