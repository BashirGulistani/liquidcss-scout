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






