import unittest
from liquidcss_scout.scanner import ScanResult
from liquidcss_scout.pruner import prune_css


class TestBasic(unittest.TestCase):
    def test_prune_safe_keeps_dynamic_candidates(self):
        css = """
        .used { color: red; }
        .maybe { color: blue; }
        .unused { color: green; }
        """


