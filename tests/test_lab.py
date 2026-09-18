import tempfile
import unittest
from pathlib import Path

from kachysec.lab import (
    LabDefinition,
    build_lab_plans,
    discover_labs,
    render_lab_plans,
)


class LabTests(unittest.TestCase):
    def test_discovery_only_returns_existing_definitions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs" / "containers").mkdir(parents=True)
            labs = discover_labs(root)
        self.assertEqual([lab.name for lab in labs], ["containers"])

    def test_lab_plan_is_review_only(self) -> None:
        labs = [LabDefinition("demo", "labs/demo", "podman", "authorized training", "isolated")]
        plans = build_lab_plans(labs)
        self.assertEqual(plans[0].action, "review-only")
        self.assertIn("No containers or virtual machines were created", render_lab_plans(plans))


if __name__ == "__main__":
    unittest.main()
