from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional

from pgtonic.spec.parse.ast_passes import maybe_to_choice
from pgtonic.spec.parse.parse import parse
from pgtonic.spec.parse.types import Base, Choice

if TYPE_CHECKING:
    from pgtonic.spec.parse.types import Base


@dataclass(eq=True, frozen=True)
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
        return parse(self.spec)

    @property
    def ast_simple(self) -> "Base":
        ast = self.ast
        return maybe_to_choice(ast)

    def to_regex(self) -> str:
        ast_simple = self.ast_simple
        return ast_simple.to_regex(self.where or {})

    def to_regexes(self) -> List[str]:
        # For efficiency. Splitting the top level
        # Choice is not strictly necessary
        ast_simple = self.ast_simple
        if isinstance(ast_simple, Choice):
            # Strip the initial group
            return [x.to_regex(self.where or {})[1:-1] for x in ast_simple.members]
        return [ast_simple.to_regex(self.where or {})]

    def is_match(self, sql: str):
        return any([re.match("^" + regex + "$", sql) for regex in self.to_regexes()])
