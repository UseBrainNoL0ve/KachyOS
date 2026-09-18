import unittest
from unittest.mock import patch

from kachysec.audit import AuditCheck, render_audit


class AuditTests(unittest.TestCase):
    def test_render_audit_contains_status_and_action(self) -> None:
        checks = [
            AuditCheck(
                "firewall",
                "WARN",
                "Firewall needs review.",
                "inactive",
                "Review the firewall configuration.",
            )
        ]
        rendered = render_audit(checks)
        self.assertIn("[WARN] firewall", rendered)
        self.assertIn("evidence: inactive", rendered)
        self.assertIn("action:", rendered)

    @patch("kachysec.audit.shutil.which", return_value=None)
    def test_audit_handles_missing_firewall_tools(self, _which) -> None:
        from kachysec.audit import collect_audit

        checks = collect_audit()
        firewall = next(check for check in checks if check.name == "firewall")
        self.assertEqual(firewall.status, "WARN")


if __name__ == "__main__":
    unittest.main()
