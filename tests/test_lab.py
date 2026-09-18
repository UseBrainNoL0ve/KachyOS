import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kachysec.lab import collect_runtimes, discover_labs, render_lab_status


class LabTests(unittest.TestCase):
    @patch("kachysec.lab.shutil.which", return_value=None)
    def test_runtime_collection_is_safe(self, _which):
        runtimes = collect_runtimes()
        self.assertTrue(runtimes)
        self.assertFalse(any(item.installed for item in runtimes))

    def test_discovery_only_returns_existing_definitions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs" / "containers").mkdir(parents=True)
            labs = discover_labs(root)
            self.assertEqual([item.name for item in labs], ["containers"])

    def test_render_is_read_only(self):
        text = render_lab_status([], [])
        self.assertIn("read-only", text)
        self.assertIn("not modified", text)


if __name__ == "__main__":
    unittest.main()
