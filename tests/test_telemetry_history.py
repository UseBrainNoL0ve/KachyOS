import tempfile
import unittest
from pathlib import Path

from kachysec.telemetry import TelemetrySnapshot
from kachysec.telemetry_history import load_snapshots, render_history, save_snapshot


class TelemetryHistoryTests(unittest.TestCase):
    def test_round_trip_and_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            for index in range(3):
                save_snapshot(
                    TelemetrySnapshot(index + 1, float(index), 1000, 500, index, 2, 10 + index),
                    path=path,
                )
            snapshots = load_snapshots(2, path=path)
            self.assertEqual(len(snapshots), 2)
            self.assertEqual(snapshots[0].processes, 12)

    def test_render_history(self):
        rendered = render_history([TelemetrySnapshot(1, 0.5, 1000, 500, 1, 2, 9)])
        self.assertIn("load 0.50", rendered)
        self.assertIn("proc 9", rendered)


if __name__ == "__main__":
    unittest.main()
