from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  
except Exception:
    yaml = None



@dataclass
class Allowlist:
    classes: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)


@dataclass
class ScoutConfig:
    project_root: str = "."
    scan_include: list[str] = field(default_factory=lambda: ["**/*.liquid", "**/*.html", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx"])
    scan_exclude: list[str] = field(default_factory=lambda: ["**/node_modules/**", "**/.git/**", "**/dist/**", "**/build/**", "**/vendor/**"])

    css_include: list[str] = field(default_factory=lambda: ["assets/**/*.css", "assets/**/*.css.liquid", "assets/**/*.scss", "assets/**/*.scss.liquid"])
    css_exclude: list[str] = field(default_factory=lambda: ["**/*.min.css", "**/*.min.css.liquid", "**/vendor/**"])


    allowlist: Allowlist = field(default_factory=Allowlist)
    keep_regex: list[str] = field(default_factory=list)

    output_dir: str = ".liquidcss-scout-out"
    mode: str = "safe"  

    write_pruned_files: bool = True
    write_patches: bool = True
    write_html_report: bool = True


def _coerce_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]



def load_config(path: str | None) -> ScoutConfig:
    if not path:
        return ScoutConfig()

    p = Path(path)
    if not p.exists():
        return ScoutConfig()




