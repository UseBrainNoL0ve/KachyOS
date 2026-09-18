import unittest
from unittest.mock import patch
from kachysec.telemetry import TelemetrySnapshot, render_telemetry

class TelemetryTests(unittest.TestCase):
    def test_render_telemetry(self):
        rendered = render_telemetry(TelemetrySnapshot(0, 1.25, 1024*1024, 512*1024, 3, 2, 120))
        self.assertIn('Listening TCP: 3', rendered)
        self.assertIn('Processes: 120', rendered)
        self.assertIn('read-only', rendered)

    @patch('kachysec.telemetry.shutil.which', return_value=None)
    def test_socket_collection_degrades_without_ss(self, _which):
        from kachysec.telemetry import _socket_counts
        self.assertEqual(_socket_counts(), (0, 0))

if __name__ == '__main__': unittest.main()