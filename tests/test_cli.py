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

    def test_baseline_diff_latest_flag(self) -> None:
        args = build_parser().parse_args(["baseline-diff", "--latest"])
        self.assertTrue(args.latest)

    def test_assistant_command(self) -> None:
        args = build_parser().parse_args(["assistant", "explain this audit warning"])
        self.assertEqual(args.command, "assistant")
        self.assertEqual(args.question, "explain this audit warning")

    def test_assistant_provider_flag(self) -> None:
        args = build_parser().parse_args(["assistant", "--providers"])
        self.assertTrue(args.providers)

    def test_baseline_output_options(self) -> None:
        args = build_parser().parse_args(["baseline", "--format", "json", "--output", "report.json"])
        self.assertEqual(args.format, "json")
        self.assertEqual(str(args.output), "report.json")


if __name__ == "__main__":
    unittest.main()
