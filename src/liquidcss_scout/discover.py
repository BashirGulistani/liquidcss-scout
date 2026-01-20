from __future__ import annotations
from pathlib import Path
from fnmatch import fnmatch


def _matches_any(path_str: str, patterns: list[str]) -> bool:
    return any(fnmatch(path_str, pat) for pat in patterns)


