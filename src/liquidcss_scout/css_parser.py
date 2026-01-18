import re
from dataclasses import dataclass
from typing import List, Set, Tuple

RULE_RE = re.compile(r"(?s)([^{}]+)\{([^{}]*)\}")
COMMENT_RE = re.compile(r"(?s)/\*.*?\*/")


TOKEN_RE = re.compile(r"([.#])([A-Za-z0-9_-]+)")







