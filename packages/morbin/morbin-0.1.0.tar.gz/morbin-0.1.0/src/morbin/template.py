from morbin import Morbin, Output


class Program(Morbin):
    def program(self, args: str = "") -> Output:
        """Base function for executing `program` commands.

        Higher level commands should be built on this function and return its output."""
        return self.execute("program", args)
