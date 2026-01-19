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




