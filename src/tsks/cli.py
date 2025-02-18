import argparse
import subprocess
import sys
import tomllib


def get_available_tasks() -> dict[str, str]:
    try:
        with open("pyproject.toml", "rb") as f:
            available_tasks: dict[str, str] | None = (
                tomllib.load(f).get("tool", {}).get("tsks")
            )
    except FileNotFoundError:
        print("Error: pyproject.toml file not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading pyproject.toml. {e}")
        sys.exit(1)
    if not available_tasks:
        print(
            "Error: Tasks not found. Add tasks in pyproject.toml under [tool.tsks]."
        )
        sys.exit(1)
    return available_tasks


def run_tasks(tasks: list[str]) -> None:
    available_tasks = get_available_tasks()
    for task in tasks:
        command = available_tasks.get(task)
        if not command:
            print(f"Error: Task '{task}' not found in pyproject.toml.")
            sys.exit(1)
        print(f"\033[1m{command}\033[0m")
        result = subprocess.run(command.split(), capture_output=True, text=True)
        out = result.stdout
        if out:
            print(out)
        err = result.stderr
        if err:
            print(err)


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="tsks", description="simple task runner for python projects"
    )
    parser.add_argument("tasks", type=str, nargs="+")
    tasks: list[str] = parser.parse_args().tasks
    run_tasks(tasks)
