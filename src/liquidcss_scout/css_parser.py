import re
from dataclasses import dataclass
from typing import List, Set, Tuple

RULE_RE = re.compile(r"(?s)([^{}]+)\{([^{}]*)\}")
COMMENT_RE = re.compile(r"(?s)/\*.*?\*/")


TOKEN_RE = re.compile(r"([.#])([A-Za-z0-9_-]+)")





@dataclass(frozen=True)
class CssRule:
    selectors_raw: str
    body: str
    selectors: List[str]
    class_tokens: Set[str]
    id_tokens: Set[str]


def strip_comments(css: str) -> str:
    return COMMENT_RE.sub("", css)





