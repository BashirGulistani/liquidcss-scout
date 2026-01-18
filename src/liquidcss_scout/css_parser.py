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






def parse_css_rules(css: str) -> List[CssRule]:
    css = strip_comments(css)
    rules: List[CssRule] = []

    for m in RULE_RE.finditer(css):
        selectors_raw = m.group(1).strip()
        body = m.group(2)
        if not selectors_raw:
            continue

        selectors = [s.strip() for s in selectors_raw.split(",") if s.strip()]

        class_tokens: Set[str] = set()
        id_tokens: Set[str] = set()
        for sel in selectors:
            for kind, token in TOKEN_RE.findall(sel):
                if kind == ".":
                    class_tokens.add(token)
                else:
                    id_tokens.add(token)

        rules.append(CssRule(
            selectors_raw=selectors_raw,
            body=body,
            selectors=selectors,
            class_tokens=class_tokens,
            id_tokens=id_tokens,
        ))

    return rules

