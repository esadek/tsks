import io
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

from tsks.cli import get_available_tasks, run_command


class TestGetAvailableTasks(unittest.TestCase):
    def setUp(self) -> None:
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

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

    @patch("builtins.open", side_effect=FileNotFoundError())
    def test_file_not_found(self, mock_file: MagicMock) -> None:
        with self.assertRaises(SystemExit) as cm:
            get_available_tasks()
        mock_file.assert_called()
        self.assertEqual(cm.exception.code, 1)
        output = self.captured_output.getvalue()
        self.assertIn("Error: pyproject.toml file not found.", output)

    @patch("builtins.open", new_callable=mock_open, read_data="[package]\n")
    @patch("tomllib.load")
    def test_no_tasks_in_file(self, mock_load: MagicMock, mock_file: MagicMock) -> None:
        mock_load.return_value = {"package": {}}
        with self.assertRaises(SystemExit) as cm:
            get_available_tasks()
        mock_file.assert_called_once_with("pyproject.toml", "rb")
        self.assertEqual(cm.exception.code, 1)
        output = self.captured_output.getvalue()
        self.assertIn(
            "Error: Tasks not found. Add tasks in pyproject.toml under [tool.tsks].",
            output,
        )

    @patch("builtins.open", side_effect=PermissionError())
    def test_permission_error(self, mock_file: MagicMock) -> None:
        with self.assertRaises(SystemExit) as cm:
            get_available_tasks()
        mock_file.assert_called()
        self.assertEqual(cm.exception.code, 1)
        output = self.captured_output.getvalue()
        self.assertIn("An error occurred while reading pyproject.toml.", output)


class TestRunCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

    @patch("subprocess.run")
    def test_run_command_success(self, mock_run: MagicMock) -> None:
        mock_run.return_value.stdout = "Command output"
        mock_run.return_value.stderr = ""
        run_command("echo 'Hello, World!'")
        output = self.captured_output.getvalue()
        self.assertIn("Hello, World!", output)
        self.assertIn("Command output", output)

    @patch("subprocess.run")
    def test_run_command_error(self, mock_run: MagicMock) -> None:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "Command error"
        run_command("invalid_command")
        output = self.captured_output.getvalue()
        self.assertIn("Command error", output)


if __name__ == "__main__":
    unittest.main()
