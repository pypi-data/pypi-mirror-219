# morbin

Base class for creating modules that are bindings for command line tools.

## Installation

Install with:

<pre>
pip install morbin
</pre>

## Usage

The easiest way to start is to use the bundled template generator.<br>
The only argument it requires is the name of the program you want to create bindings for.

As an example we'll do Git.

Running `morbin git` in your terminal will produce a file named `git.py` in your current directory.<br>
It should look like this:
![](/imgs/template.png)
Additional functions should be built on top of this `git` function and return its output.<br>

After adding functions for `git add`, `git commit`, and `git log` the class should look like this:
![](/imgs/functions.png)

The `Output` object each function returns is a `dataclass` with three fields: `return_code`, `stdout`, and `stderr`.<br>
<pre>
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
</pre>


By default `stdout` and `stderr` are not captured.<br>
They are sent to wherever they normally would be and the `stdout` and `stderr` fields of the `Output` object will be empty strings.<br>
`stdout` and `stderr` can be captured by either setting the `capture_output` property of a class instance to `True` 
or by using the `capturing_output` context manager as demonstrated below:
![](/imgs/use.png)