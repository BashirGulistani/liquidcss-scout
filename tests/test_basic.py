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


        scan = ScanResult(
            classes={"used"},
            ids=set(),
            dynamic_classes={"maybe"},
            dynamic_ids=set(),
            files_scanned=1,
        )

        pruned, report = prune_css(css, scan, mode="safe")
        self.assertIn(".used", pruned)
        self.assertIn(".maybe", pruned)   
        self.assertNotIn(".unused", pruned) 

        self.assertEqual(report.removed_rules, 1)

    def test_prune_aggressive_removes_maybe(self):
        css = ".maybe{a:b}.used{c:d}"
        scan = ScanResult(
            classes={"used"},
            ids=set(),
            dynamic_classes={"maybe"},
            dynamic_ids=set(),
            files_scanned=1,
        )

        pruned, report = prune_css(css, scan, mode="aggressive")
        self.assertIn(".used", pruned)
        self.assertNotIn(".maybe", pruned)


if __name__ == "__main__":
    unittest.main()
