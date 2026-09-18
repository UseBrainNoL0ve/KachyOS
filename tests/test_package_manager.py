import unittest

from unittest.mock import patch

from kachysec.package_manager import build_install_plan, package_state
from kachysec.tools import ToolSpec


class PackageManagerTests(unittest.TestCase):
    def test_build_install_plan_is_unique_and_non_executing(self) -> None:
        specs = (
            ToolSpec("A", "a", "test", "A", ("a",), ("pkg-a", "pkg-shared")),
            ToolSpec("B", "b", "test", "B", ("b",), ("pkg-shared", "pkg-b")),
        )
        self.assertEqual(build_install_plan(specs), ["pkg-a", "pkg-shared", "pkg-b"])

    @patch("kachysec.package_manager.pacman_available", return_value=False)
    def test_package_state_without_pacman(self, _available) -> None:
        self.assertFalse(package_state("anything").installed)


if __name__ == "__main__":
    unittest.main()
