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



def _read_text(path: str) -> str:

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1") as f:
            return f.read()


def _split_classes(value: str) -> List[str]:
   
    value = value.strip()
    if not value:
        return []
    return [c for c in re.split(r"\s+", value) if c]




def scan_project(root: str, *, exts: Set[str] | None = None) -> ScanResult:

    exts = exts or DEFAULT_TEXT_EXTS

    classes: Set[str] = set()
    ids: Set[str] = set()
    dyn_classes: Set[str] = set()
    dyn_ids: Set[str] = set()
    count = 0

    for path in _iter_files(root, exts):
        count += 1
        text = _read_text(path)

        for m in CLASS_RE.finditer(text):
            raw = m.group(1)
            if DYNAMIC_LIQUID_RE.search(raw):
 
                for token in _split_classes(DYNAMIC_LIQUID_RE.sub(" ", raw)):
                    dyn_classes.add(token)
            else:
                for token in _split_classes(raw):
                    classes.add(token)

        for m in ID_RE.finditer(text):
            raw = m.group(1).strip()
            if not raw:
                continue
            if DYNAMIC_LIQUID_RE.search(raw):
                cleaned = DYNAMIC_LIQUID_RE.sub(" ", raw).strip()
                if cleaned:
                    dyn_ids.add(cleaned)
            else:
                ids.add(raw)


        for m in JS_CLASS_ADD_RE.finditer(text):
            value = m.group(1)
            if value:
                classes.add(value)

        for m in JS_CLASSNAME_RE.finditer(text):
            value = m.group(1)
            for token in _split_classes(value):
                classes.add(token)

        for m in JS_QS_RE.finditer(text):
            kind = m.group(1)
            sel = m.group(2).strip()
            if not sel:
                continue

            if kind == ".":
   
                for token in re.findall(r"[A-Za-z0-9_-]+", sel):
                    classes.add(token)
            elif kind == "#":
                token = re.match(r"[A-Za-z0-9_-]+", sel)
                if token:
                    ids.add(token.group(0))

    return ScanResult(
        classes=classes,
        ids=ids,
        dynamic_classes=dyn_classes,
        dynamic_ids=dyn_ids,
        files_scanned=count,
    )





