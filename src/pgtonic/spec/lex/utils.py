
from typing import Tuple, List, Dict, Callable

def build_consumer(charset: List[str]) -> Callable[[str], Tuple[str, str]]:
    """Return a callable that consume anything in *charset*
    and returns a tuple of the consumed and unconsumed text"""

    def consumer(text: str) -> Tuple[str, str]:
        consumed = []
        start_ix = 0

        should_continue = True
        while should_continue:
            should_continue = False

            for chars in charset:
                if text[start_ix:].startswith(chars):
                    start_ix += len(chars)
                    consumed.append(chars)
                    should_continue = True

        token = "".join(consumed)
        return token, text[len(token) :]

    return consumer


