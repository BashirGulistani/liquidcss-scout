import os
import re
from dataclasses import dataclass
from typing import Iterable, Set, Dict, List, Tuple


CLASS_RE = re.compile(r'class\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
ID_RE = re.compile(r'id\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)


JS_CLASS_ADD_RE = re.compile(r'\.classList\.(?:add|remove|toggle)\(\s*["\']([^"\']+)["\']', re.IGNORECASE)
JS_CLASSNAME_RE = re.compile(r'\.className\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
JS_QS_RE = re.compile(r'querySelector(?:All)?\(\s*["\']([.#])([^"\']+)["\']', re.IGNORECASE)


