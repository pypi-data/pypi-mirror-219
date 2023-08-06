import argparse
import shlex
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass

from pathier import Pathier
from typing_extensions import Self

root = Pathier(__file__).parent


@dataclass
class Output:
    """Dataclass representing the output of a terminal command.

    #### Fields:
    * `return_code: list[int]`
    * `stdout: str`
    * `stderr: str`"""

    return_code: list[int]
    stdout: str = ""
    stderr: str = ""

    def __add__(self, output: Self) -> Self:
        return Output(
            self.return_code + output.return_code,
            self.stdout + output.stdout,
            self.stderr + output.stderr,
        )


class Morbin:
    def __init__(self, capture_output: bool = False, shell: bool = False):
        """Command bindings should return an `Output` object.

        If `capture_output` is `True` or the `capturing_output` context manager is used,
        the command's output will be available via `Output.stdout` and `Output.stderr`.

        This property can be used to parse and use the command output or to simply execute commands "silently".

        The return code will also be available via `Output.return_code`.

        If `shell` is `True`, commands will be executed in the system shell (necessary on Windows for builtin shell commands like `cd` and `dir`).

        [Security concerns using shell = True](https://docs.python.org/3/library/subprocess.html#security-considerations)

        """
        self.capture_output = capture_output
        self.shell = shell

    @property
    def capture_output(self) -> bool:
        """If `True`, member functions will return the generated `stdout` as a string,
        otherwise they return the command's exit code as a string (so my type checker doesn't throw a fit about ints.)."""
        return self._capture_output

    @capture_output.setter
    def capture_output(self, should_capture: bool):
        self._capture_output = should_capture

    @property
    def shell(self) -> bool:
        """If `True`, commands will be executed in the system shell."""
        return self._shell

    @shell.setter
    def shell(self, should_use: bool):
        self._shell = should_use

    @contextmanager
    def capturing_output(self):
        """Ensures `self.capture_output` is `True` while within the context.

        Upon exiting the context, `self.capture_output` will be set back to whatever it was when the context was entered."""
        original_state = self.capture_output
        self.capture_output = True
        yield self
        self.capture_output = original_state

    def execute(self, program: str, args: str) -> Output:
        command = [program] + shlex.split(args)
        if self.capture_output:
            output = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=self.shell,
            )
            return Output([output.returncode], output.stdout, output.stderr)
        else:
            output = subprocess.run(command, shell=self.shell)
            return Output([output.returncode])


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "name",
        type=str,
        help=""" The program name to create a template subclass of Morbin for. """,
    )
    args = parser.parse_args()

    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    template = (root / "template.py").read_text()
    template = template.replace("Program", args.name.capitalize()).replace(
        "program", args.name
    )
    (Pathier.cwd() / f"{args.name}.py").write_text(template)


if __name__ == "__main__":
    main(get_args())
