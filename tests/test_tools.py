import unittest
from unittest.mock import patch

from kachysec.tools import check_tools, summarize_tools


class ToolCatalogTests(unittest.TestCase):
    @patch("kachysec.tools.shutil.which")
    def test_check_tools(self, which):
        which.side_effect = lambda binary: "/usr/bin/" + binary if binary == "nmap" else None
        items = check_tools()
        nmap = next(item for item in items if item["binary"] == "nmap")
        self.assertTrue(nmap["installed"])
        summary = summarize_tools(items)
        self.assertEqual(summary["installed"], 1)
        self.assertEqual(summary["total"], len(items))


if __name__ == "__main__":
    unittest.main()
