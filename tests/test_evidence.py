import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kachysec.evidence import diff_baselines, latest_baselines, render_diff, save_baseline

class EvidenceTests(unittest.TestCase):
    def test_diff_detects_added_removed_and_changed_fields(self):
        before = {"platform": {"python": "3.11"}, "package_count": 10, "old": True}
        after = {"platform": {"python": "3.12"}, "package_count": 12, "new": True}
        diff = diff_baselines(before, after)
        self.assertEqual(diff.added, ("new",))
        self.assertEqual(diff.removed, ("old",))
        self.assertEqual(diff.changed, ("package_count", "platform.python"))

    def test_save_baseline_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = save_baseline({"schema_version": 1}, path=Path(tmp))
            self.assertTrue(path.exists())
            self.assertEqual(json.loads(path.read_text()), {"schema_version": 1})

    def test_latest_baselines_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index in range(3):
                (root / f"baseline-20260101T00000{index}Z.json").write_text("{}")
            with patch("kachysec.evidence.baseline_store", return_value=root):
                self.assertEqual(len(latest_baselines(2)), 2)

    def test_render_diff_is_human_readable(self):
        diff = diff_baselines({"a": 1}, {"a": 2, "b": 3})
        rendered = render_diff(diff, before=Path("before.json"), after=Path("after.json"))
        self.assertIn("Changed fields: **1**", rendered)
        self.assertIn("`b`", rendered)

if __name__ == "__main__":
    unittest.main()
