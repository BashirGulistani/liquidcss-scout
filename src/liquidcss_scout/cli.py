import argparse
import json
import os
from pathlib import Path

from .scanner import scan_project
from .pruner import prune_css


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()








