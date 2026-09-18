import unittest

from kachysec.updates import _parse_pacman_updates, render_updates


class UpdateTests(unittest.TestCase):
    def test_parse_pacman_updates(self) -> None:
        updates = _parse_pacman_updates(
            "linux 6.16.1.arch1-1 -> 6.16.2.arch1-1\n"
            "python 3.13.7-1 -> 3.13.7-2 [extra]\n"
        )
        self.assertEqual(len(updates), 2)
        self.assertEqual(updates[0].name, "linux")
        self.assertEqual(updates[0].current, "6.16.1.arch1-1")
        self.assertEqual(updates[1].available, "3.13.7-2")

    def test_render_empty(self) -> None:
        rendered = render_updates([])
        self.assertIn("No pending package updates", rendered)
        self.assertIn("read-only", rendered)


if __name__ == "__main__":
    unittest.main()
