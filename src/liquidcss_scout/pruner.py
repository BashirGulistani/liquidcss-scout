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




def prune_css(css: str, scan: ScanResult, *, mode: str = "safe") -> tuple[str, PruneReport]:

    if mode not in ("safe", "aggressive"):
        raise ValueError("mode must be 'safe' or 'aggressive'")

    rules = parse_css_rules(css)

    known_classes = set(scan.classes)
    known_ids = set(scan.ids)
    dyn_classes = set(scan.dynamic_classes)
    dyn_ids = set(scan.dynamic_ids)

    kept_chunks: List[str] = []
    kept_selectors: List[str] = []
    removed_selectors: List[str] = []
    maybe_selectors: List[str] = []
    kept = removed = maybe = 0

    for r in rules:
        used_class = _is_used(r.class_tokens, known_classes)
        used_id = _is_used(r.id_tokens, known_ids)

        is_used = (used_class or used_id)

        is_maybe = _is_maybe(r.class_tokens, dyn_classes) or _is_maybe(r.id_tokens, dyn_ids)




        decision = "keep"
        if not is_used:
            if is_maybe and mode == "safe":
                decision = "maybe"
            else:
                decision = "remove"

        if decision == "keep":
            kept += 1
            kept_selectors.append(r.selectors_raw)
            kept_chunks.append(f"{r.selectors_raw}{{{r.body}}}")
        elif decision == "maybe":
            maybe += 1
            maybe_selectors.append(r.selectors_raw)
            kept_chunks.append(f"{r.selectors_raw}{{{r.body}}}")
        else:
            removed += 1
            removed_selectors.append(r.selectors_raw)

    pruned_css = "\n".join(kept_chunks).strip() + ("\n" if kept_chunks else "")
    report = PruneReport(
        kept_rules=kept,
        removed_rules=removed,
        maybe_rules=maybe,
        kept_selectors=kept_selectors,
        removed_selectors=removed_selectors,
        maybe_selectors=maybe_selectors,
    )
    return pruned_css, report


