"""helper tool"""
__version__ = "0.1.3"


from typing import TextIO


class EnhancedWriter:
    def __init__(self, file: TextIO | str) -> None:
        if isinstance(file, str):
            self.writer = open(file, mode="w", encoding="utf-8")
        else:
            self.writer = file

    @property
    def name(self):
        return self.writer.name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        return True

    def __del__(self):
        if not self.writer.closed:
            self.writer.close()

    def write(self, s: str):
        return self.writer.write(s)

    def writeln(self, s: str = "", intent: int = 0):
        if s is not str:
            s = str(s)
        if intent == 0:
            return self.writer.write(s + "\n")
        lines = s.splitlines(keepends=True)
        for line in lines:
            self.writer.write(f"{' '*intent}{line}")
        self.writer.write("\n")
