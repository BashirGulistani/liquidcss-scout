import os
import re
from dataclasses import dataclass
from typing import Iterable, Set, Dict, List, Tuple


CLASS_RE = re.compile(r'class\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
ID_RE = re.compile(r'id\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)


JS_CLASS_ADD_RE = re.compile(r'\.classList\.(?:add|remove|toggle)\(\s*["\']([^"\']+)["\']', re.IGNORECASE)
JS_CLASSNAME_RE = re.compile(r'\.className\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
JS_QS_RE = re.compile(r'querySelector(?:All)?\(\s*["\']([.#])([^"\']+)["\']', re.IGNORECASE)


DYNAMIC_LIQUID_RE = re.compile(r'{{.*?}}', re.DOTALL)


DEFAULT_TEXT_EXTS = {".liquid", ".html", ".htm", ".js", ".ts", ".jsx", ".tsx"}



@dataclass(frozen=True)
class ScanResult:
    classes: Set[str]
    ids: Set[str]
    dynamic_classes: Set[str]
    dynamic_ids: Set[str]
    files_scanned: int


def _iter_files(root: str, exts: Set[str]) -> Iterable[str]:
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            _, ext = os.path.splitext(fn)
            if ext.lower() in exts:
                yield os.path.join(dirpath, fn)


