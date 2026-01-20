from __future__ import annotations
from pathlib import Path
from fnmatch import fnmatch


def _matches_any(path_str: str, patterns: list[str]) -> bool:
    return any(fnmatch(path_str, pat) for pat in patterns)


def discover_files(root: str, includes: list[str], excludes: list[str]) -> list[str]:
    r = Path(root).resolve()
    out: list[str] = []
    for p in r.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(r)).replace("\\", "/")
        if includes and not _matches_any(rel, includes):
            continue
        if excludes and _matches_any(rel, excludes):
            continue
        out.append(str(p))
    return sorted(out)
