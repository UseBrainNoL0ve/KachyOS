import unittest
from unittest.mock import patch

from kachysec.tool_manager import build_install_plan
from kachysec.tools import ToolSpec


class ToolManagerTests(unittest.TestCase):
    def test_empty_plan(self) -> None:
        self.assertEqual(build_install_plan([]).packages, ())

    @patch("kachysec.tool_manager.shutil.which", return_value=None)
    def test_plan_is_non_destructive_without_pacman(self, _which) -> None:
        plan = build_install_plan([ToolSpec("demo", "demo", "test", "demo", ("demo",), ("demo",))])
        self.assertEqual(plan.packages, ())

    @patch("kachysec.tool_manager._available_packages", return_value={"nmap"})
    @patch("kachysec.tool_manager._installed_packages", return_value=set())
    @patch("kachysec.tool_manager.shutil.which", return_value="/usr/bin/pacman")
    def test_plan_batches_package_resolution(self, _which, _installed, _available) -> None:
        spec = ToolSpec("Nmap", "nmap", "network", "demo", ("nmap",), ("nmap",))
        plan = build_install_plan([spec])
        self.assertEqual(plan.packages, ("nmap",))


if __name__ == "__main__":
    unittest.main()
