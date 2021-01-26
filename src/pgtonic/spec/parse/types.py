from typing import List
from dataclasses import dataclass


@dataclass
class Base:
    pass


@dataclass
class Statement:
    ast: List[Base]

##############
# Leaf Nodes #
##############


@dataclass
class Leaf:
    content: str


@dataclass
class Literal(Leaf):
    pass


@dataclass
class Argument(Leaf):
    """User input"""
    pass


@dataclass
class Repeat(Leaf):
    """Comma separated"""
    pass

@dataclass
class Pipe(Leaf):
    pass



###################
# Group Nodes
###################


@dataclass
class Group(Base):
    members: List[Base]

@dataclass
class Choice(Group):
    pass

@dataclass
class InParens(Group):
    pass

@dataclass
class Maybe(Group):
    pass
