from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional

from pgtonic.spec.lex.lex import lex
from pgtonic.spec.parse.parse import _parse
from pgtonic.spec.parse.stream_passes import filter_whitespace
from pgtonic.spec.parse.types import Base, Group
from pgtonic.spec.parse.ast_passes import maybe_to_choice
if TYPE_CHECKING:
    from pgtonic.spec.parse.types import Base, Group


@dataclass
class Template:
    original: str
    corrected: Optional[str] = None
    where: Optional[Dict[str, "Template"]] = None

    @property
    def spec(self) -> str:
        """Return the corrected spec if it exists, otherwise the original"""
        return self.corrected or self.original

    @property
    def ast(self) -> "Base":
        tstream0 = lex(self.spec)
        tstream1 = filter_whitespace(tstream0)
        nodes =_parse(tstream1)  # type: ignore
        

        if isinstance(nodes, list):
            return Group(nodes)
        return nodes

    @property
    def ast_simple(self) -> "Base":
        ast = self.ast
        return maybe_to_choice(ast)

    def to_regex(self) -> str:
        return self.ast_simple.to_regex(self.where or {})
