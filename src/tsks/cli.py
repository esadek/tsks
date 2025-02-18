import argparse
import shlex
import subprocess
import sys
import tomllib

type TasksDict = dict[str, str | list[str]]


def get_available_tasks() -> TasksDict:
    try:
        with open("pyproject.toml", "rb") as f:
            available_tasks: TasksDict | None = (
                tomllib.load(f).get("tool", {}).get("tsks")
            )
    except FileNotFoundError:
        print("Error: pyproject.toml file not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading pyproject.toml. {e}")
        sys.exit(1)
    if not available_tasks:
        print("Error: Tasks not found. Add tasks in pyproject.toml under [tool.tsks].")
        sys.exit(1)
    return available_tasks


def run_command(command: str) -> None:
    print(f"\033[1m{command}\033[0m")
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)
    out = result.stdout
    if out:
        print(out)
    err = result.stderr
    if err:
        print(err)


def run_tasks(tasks: list[str]) -> None:
    available_tasks = get_available_tasks()
    for task in tasks:
        commands = available_tasks.get(task)
        if not commands:
            print(f"Error: Task '{task}' not found in pyproject.toml.")
            sys.exit(1)
        if isinstance(commands, str):
            run_command(commands)
        elif isinstance(commands, list):
            for command in commands:
                run_command(command)


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="tsks", description="simple task runner for python projects"
    )
    parser.add_argument("tasks", type=str, nargs="+", help="tasks to run")
    tasks: list[str] = parser.parse_args().tasks
    run_tasks(tasks)
