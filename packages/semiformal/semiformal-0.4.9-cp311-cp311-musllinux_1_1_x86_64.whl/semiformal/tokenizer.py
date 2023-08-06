from typing import List, Tuple

from semiformal import _tokenizer
from semiformal.token_types import TokenType

def tokens(text: str) -> Tuple[Tuple[int, int, int]]:
    return _tokenizer.tokens(text)


def tokenize(text: str, exclude_token_types: List[[TokenType, int]]=None) -> List[Tuple[str, TokenType]]:
    enum_values = TokenType._value2member_map_
    token_classes = _tokenizer.tokenize(text)
    if exclude_token_types:
        exclude_token_types = [getattr(c, 'value', c) for c in exclude_token_types]
        return [(s, enum_values[c]) for s, c in token_classes if c not in exclude_token_types]
    return [(s, enum_values[c]) for s, c in token_classes]

