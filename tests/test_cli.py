import unittest

from kachysec.cli import build_parser


class CliTests(unittest.TestCase):
    def test_tools_plan_flag(self) -> None:
        args = build_parser().parse_args(["tools", "--plan"])
        self.assertTrue(args.plan)

    def test_lab_command(self) -> None:
        args = build_parser().parse_args(["lab"])
        self.assertEqual(args.command, "lab")

    def test_lab_plan_flag(self) -> None:
        args = build_parser().parse_args(["lab", "--plan"])
        self.assertTrue(args.plan)

    def test_baseline_output_options(self) -> None:
        args = build_parser().parse_args(["baseline", "--format", "json", "--output", "report.json"])
        self.assertEqual(args.format, "json")
        self.assertEqual(str(args.output), "report.json")


if __name__ == "__main__":
    unittest.main()
