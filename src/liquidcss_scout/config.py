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




