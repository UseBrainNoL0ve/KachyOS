import unittest
from unittest.mock import patch

from kachysec.gui import dashboard_snapshot


class GuiTests(unittest.TestCase):
    @patch("kachysec.gui.discover_labs", return_value=[])\n    @patch("kachysec.gui.collect_runtimes", return_value=[])\n    @patch("kachysec.gui.collect_updates", return_value=[])
    @patch("kachysec.gui.collect_audit", return_value=[])
    @patch("kachysec.gui.collect_status", return_value={"runtimes": {"podman": True}})
    @patch(
        "kachysec.gui.check_tools",
        return_value=[
            {"name": "Nmap", "category": "network", "purpose": "discovery", "installed": True}
        ],
    )
    def test_snapshot_uses_shared_read_only_services(
        self, _tools, _status, _audit, _updates, _runtimes, _labs
    ) -> None:
        snapshot = dashboard_snapshot()
        self.assertEqual(snapshot["tool_summary"]["installed"], 1)
        self.assertEqual(len(snapshot["updates"]), 0)
        self.assertTrue(snapshot["status"]["runtimes"]["podman"])


if __name__ == "__main__":
    unittest.main()
