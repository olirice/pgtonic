from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Dict, List

from pgtonic.spec import regex as r

if TYPE_CHECKING:
    from pgtonic.spec.template import Template


class ToRegexMixin:
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        raise NotImplementedError()


@dataclass
class Base(ToRegexMixin):
    pass


##############
# Leaf Nodes #
##############


def w(add_whitespace: bool) -> str:
    return r.WHITESPACE if add_whitespace else ""


@dataclass
class Leaf(Base):
    content: str

    def to_regex(self, where: Dict[str, "Template"]) -> str:
        # Is abstract, should never be in AST
        raise NotImplementedError(self.__class__.__name__)


@dataclass
class Literal(Leaf):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        return str(self.content)


@dataclass
class Argument(Leaf):
    """User input"""

    def to_regex(self, where: Dict[str, "Template"]) -> str:
        template = where[self.content]
        # TODO: Add a named capture group
        #return f'(?:<{self.content}>' + template.to_regex() + ')'
        return template.to_regex()


@dataclass
class Pipe(Leaf):
    pass


@dataclass
class Nothing(Leaf):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        return "()"


@dataclass
class UnqualifiedName(Leaf):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        return r.UNQUALIFIED_NAME


@dataclass
class QualifiedName(Leaf):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        return r.QUALIFIED_NAME


@dataclass
class Name(Leaf):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        return r.NAME


###################
# Group Nodes
###################


@dataclass
class Group(Base):
    members: List[Base]

    def to_regex(self, where: Dict[str, "Template"]) -> str:
        result = "("
        # TODO: Optional whitespace befoer InParens
        for ix, x in enumerate(self.members):
            if ix == 0:
                result += x.to_regex(where)
            elif isinstance(x, InParens):
                result += r.OPTIONAL_WHITESPACE + x.to_regex(where)
            else:
                result += r.WHITESPACE + x.to_regex(where)

        result += ")"
        return result


@dataclass
class Choice(Group):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        result = "("
        result += "|".join([x.to_regex(where) for x in self.members])
        result += ")"
        return result


@dataclass
class InParens(Group):
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        result = r"\(" + r.OPTIONAL_WHITESPACE
        result += r.WHITESPACE.join([x.to_regex(where) for x in self.members])
        result += r.OPTIONAL_WHITESPACE + r"\)"
        return result


##################
# Modifier Nodes #
##################


@dataclass
class Modifier(Base):
    wraps: Base


@dataclass
class Repeat(Modifier):
    wraps: Base

    delimiter_regex: ClassVar[str]

    def to_regex(self, where: Dict[str, "Template"]) -> str:
        self_reg = self.wraps.to_regex(where)
        result = "(" + self_reg + ")"
        result += "(" + r.OPTIONAL_WHITESPACE + self.delimiter_regex + r.OPTIONAL_WHITESPACE + self_reg + ")*"
        return result


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
    def to_regex(self, where: Dict[str, "Template"]) -> str:
        raise NotImplementedError()
