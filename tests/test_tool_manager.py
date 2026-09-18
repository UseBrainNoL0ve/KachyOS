import unittest

from kachysec.tool_manager import InstallPlan, render_plan


class ToolManagerTests(unittest.TestCase):
    def test_empty_plan(self) -> None:
        self.assertIn("No installable", render_plan(InstallPlan((), ())))

    def test_plan_is_non_destructive(self) -> None:
        text = render_plan(InstallPlan(("nmap",), ("Nmap",)))
        self.assertIn("plan only", text)


if __name__ == "__main__":
    unittest.main()
