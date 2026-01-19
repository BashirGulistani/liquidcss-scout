import argparse
import json
import os
from pathlib import Path

from .scanner import scan_project
from .pruner import prune_css


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main() -> None:
    p = argparse.ArgumentParser(
        prog="liquidcss-scout",
        description="Find unused CSS selectors in Liquid/HTML/JS projects and safely prune CSS.",
    )



    p.add_argument("project_root", help="Path to your theme/project root (contains .liquid/.html/.js)")
    p.add_argument("--css", required=True, help="Path to CSS file to analyze/prune")
    p.add_argument("--mode", choices=["safe", "aggressive"], default="safe", help="Pruning mode")
    p.add_argument("--out-css", default=None, help="Write pruned CSS to this path")
    p.add_argument("--out-report", default=None, help="Write JSON report to this path")
    args = p.parse_args()

    scan = scan_project(args.project_root)
    css_text = _read(args.css)

    pruned, report = prune_css(css_text, scan, mode=args.mode)

    payload = {
        "files_scanned": scan.files_scanned,
        "classes_found": len(scan.classes),
        "ids_found": len(scan.ids),
        "dynamic_class_candidates": len(scan.dynamic_classes),
        "dynamic_id_candidates": len(scan.dynamic_ids),
        "kept_rules": report.kept_rules,
        "maybe_rules": report.maybe_rules,
        "removed_rules": report.removed_rules,
        "removed_selectors": report.removed_selectors[:300], 
        "maybe_selectors": report.maybe_selectors[:300],
    }

    if args.out_css:
        _write(args.out_css, pruned)
        print(f"Wrote pruned CSS -> {args.out_css}")
    else:
        print(json.dumps(payload, indent=2))

    if args.out_report:
        _write(args.out_report, json.dumps(payload, indent=2) + "\n")
        print(f"Wrote report -> {args.out_report}")
