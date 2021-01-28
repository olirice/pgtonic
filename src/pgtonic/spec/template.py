from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional

from pgtonic.spec.lex.lex import lex
from pgtonic.spec.parse.parse import _parse
from pgtonic.spec.parse.stream_passes import filter_whitespace
from pgtonic.spec.parse.types import apply_whitespace

if TYPE_CHECKING:
    from pgtonic.spec.parse.types import Base


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
    def ast(self) -> List["Base"]:
        tstream0 = lex(self.spec)
        tstream1 = filter_whitespace(tstream0)
        return _parse(tstream1)  # type: ignore

    def to_regex(self) -> str:
        # Recursively convert where template to ast
        return apply_whitespace(self.ast, self.where or {})
