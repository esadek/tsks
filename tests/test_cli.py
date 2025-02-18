import unittest
from unittest.mock import MagicMock, mock_open, patch

from tsks.cli import get_available_tasks


class TestGetAvailableTasks(unittest.TestCase):
    @patch(
        "builtins.open", new_callable=mock_open, read_data="[tool.tsks]\nkey = 'value'"
    )
    @patch("tomllib.load")
    def test_valid_file(self, mock_load: MagicMock, mock_file: MagicMock) -> None:
        expected_output = {"key": "value"}
        mock_load.return_value = {"tool": {"tsks": expected_output}}
        result = get_available_tasks()
        self.assertEqual(result, expected_output)
        mock_file.assert_called_once_with("pyproject.toml", "rb")
        mock_load.assert_called_once_with(mock_file.return_value)


if __name__ == "__main__":
    unittest.main()
