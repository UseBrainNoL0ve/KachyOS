import unittest
from unittest.mock import patch

from kachysec.baseline import CommandResult, collect, first_line, to_json, to_markdown


class BaselineTests(unittest.TestCase):
    def test_first_line(self):
        result = CommandResult("demo", True, 0, "first\nsecond", "")
        self.assertEqual(first_line(result), "first")

    @patch("kachysec.baseline.run_command")
    @patch("kachysec.baseline.shutil.which", return_value="/usr/bin/demo")
    def test_collect_has_expected_sections(self, _which, run):
        def fake(command, timeout=10):
            return CommandResult(" ".join(command), True, 0, "demo", "")

        run.side_effect = fake
        data = collect()
        self.assertEqual(data["schema_version"], 1)
        self.assertIn("security_tools", data)
        self.assertIn("firewall", data)
        self.assertIn("runtimes", data)
        self.assertIn("commands", data)

    def test_renderers(self):
        sample = {
            "collected_at": "now",
            "platform": {"system": "Linux", "release": "test", "machine": "x86_64", "python": "3.11"},
            "package_count": 42,
            "security_tools": {"nmap": True},
            "firewall": {"ufw": {"active": "inactive", "enabled": "disabled"}},
            "runtimes": {"podman": "podman version test"},
            "commands": {
                "network_addresses": {"stdout": "lo UNKNOWN 127.0.0.1"},
                "listening_sockets": {"stdout": "tcp LISTEN"},
            },
        }
        self.assertIn('"package_count": 42', to_json(sample))
        self.assertIn("# KachyOS Baseline Report", to_markdown(sample))


if __name__ == "__main__":
    unittest.main()
