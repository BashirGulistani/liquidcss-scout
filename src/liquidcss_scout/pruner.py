from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from .css_parser import parse_css_rules, strip_comments
from .scanner import ScanResult



@dataclass(frozen=True)
class PruneReport:
    kept_rules: int
    removed_rules: int
    maybe_rules: int
    kept_selectors: List[str]
    removed_selectors: List[str]
    maybe_selectors: List[str]



def _is_maybe(rule_tokens: Set[str], dynamic_tokens: Set[str]) -> bool:
    return any(t in dynamic_tokens for t in rule_tokens)


def _is_used(rule_tokens: Set[str], known_tokens: Set[str]) -> bool:
    if not rule_tokens:
        return True
    return any(t in known_tokens for t in rule_tokens)





