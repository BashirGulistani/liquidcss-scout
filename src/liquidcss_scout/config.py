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

    if yaml is None:
        raise RuntimeError("PyYAML not installed. Run: pip install pyyaml")

    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    cfg = ScoutConfig()

    cfg.project_root = str(raw.get("project_root", cfg.project_root))
    cfg.scan_include = _coerce_list(raw.get("scan_include", cfg.scan_include))
    cfg.scan_exclude = _coerce_list(raw.get("scan_exclude", cfg.scan_exclude))

    cfg.css_include = _coerce_list(raw.get("css_include", cfg.css_include))
    cfg.css_exclude = _coerce_list(raw.get("css_exclude", cfg.css_exclude))

    allow = raw.get("allowlist", {}) or {}
    cfg.allowlist = Allowlist(
        classes=_coerce_list(allow.get("classes", [])),
        ids=_coerce_list(allow.get("ids", [])),
    )

    cfg.keep_regex = _coerce_list(raw.get("keep_regex", []))
    cfg.output_dir = str(raw.get("output_dir", cfg.output_dir))
    cfg.mode = str(raw.get("mode", cfg.mode))

    cfg.write_pruned_files = bool(raw.get("write_pruned_files", cfg.write_pruned_files))
    cfg.write_patches = bool(raw.get("write_patches", cfg.write_patches))
    cfg.write_html_report = bool(raw.get("write_html_report", cfg.write_html_report))

    return cfg


