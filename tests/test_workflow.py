import unittest

from kachysec.workflow import (
    TargetScope,
    WorkflowPhase,
    build_workflow_plan,
    find_workflow,
    render_workflow_plan,
)


class WorkflowTests(unittest.TestCase):
    def test_missing_authorization_blocks_review(self):
        workflow = find_workflow("Network Service Assessment")
        plan = build_workflow_plan(workflow, TargetScope("10.0.0.10", ""))
        self.assertFalse(plan.ready_for_operator_review)
        self.assertTrue(any("Authorization" in warning for warning in plan.warnings))

    def test_explicit_authorized_scope_is_reviewable(self):
        workflow = find_workflow("Network Service Assessment")
        plan = build_workflow_plan(
            workflow,
            TargetScope("10.0.0.10", "explicitly authorized by lab owner", "authorized"),
            "Nmap",
        )
        self.assertTrue(plan.ready_for_operator_review)
        rendered = render_workflow_plan(plan)
        self.assertIn("Nmap", rendered)
        self.assertIn(WorkflowPhase.EXECUTE.value, rendered)
        self.assertIn("No command is executed", rendered)

    def test_local_host_workflow_exists(self):
        workflow = find_workflow("Local Host Hardening Review")
        self.assertEqual(workflow.steps[0].phase, WorkflowPhase.SCOPE)


if __name__ == "__main__":
    unittest.main()
