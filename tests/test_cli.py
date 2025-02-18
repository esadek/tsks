import unittest

from tsks.cli import get_available_tasks


class TestCli(unittest.TestCase):
    def test_get_available_tasks(self) -> None:
        available_tasks = get_available_tasks()
        self.assertEqual(available_tasks.get("test"), "uv run -m unittest")
        self.assertEqual(available_tasks.get("lint"), "uv run ruff check --fix")
        self.assertEqual(available_tasks.get("format"), "uv run ruff format")


if __name__ == "__main__":
    unittest.main()
