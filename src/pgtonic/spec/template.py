from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict ,TYPE_CHECKING, List
from pgtonic.spec import regex as r
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
    where: Optional[Dict[str, 'Template']] = None

    @property
    def spec(self):
        """Return the corrected spec if it exists, otherwise the original"""
        return self.corrected or self.original

    @property
    def ast(self) -> List['Base']:
        tstream0 = lex(self.spec)
        tstream1 = filter_whitespace(tstream0)
        return _parse(tstream1) # type: ignore


    def to_regex(self) -> str:
        # Recursively convert where template to where regexes
        where_regex = {k: v.to_regex() for k, v in self.where.items()} if self.where else {}
        return (
            apply_whitespace(self.ast, where_regex)
            #+ r.OPTIONAL_WHITESPACE
            #+ r.OPTIONAL_SEMICOLON
            #+ r.END_OF_LINE
        )


