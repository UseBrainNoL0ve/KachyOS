import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kachysec.operations import read_operations, run_privileged


class OperationTests(unittest.TestCase):
    def test_unconfirmed_operation_does_not_execute(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "operations.jsonl"
            with patch("kachysec.operations.log_path", return_value=path), patch("kachysec.operations.subprocess.run") as runner:
                result = run_privileged("install-tools", ("nmap",), confirm=False)
                runner.assert_not_called()
            self.assertEqual(result.returncode, 2)
            self.assertEqual(len(read_operations(path)), 1)

    def test_empty_operation_is_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "operations.jsonl"
            with patch("kachysec.operations.log_path", return_value=path):
                result = run_privileged("install-tools", (), confirm=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("No packages selected", result.output)


if __name__ == "__main__":
    unittest.main()
