from ooju.core.tokenizer import tokenize, TokenizeError
from ooju.core.parser import parse, ParseError, MultiParseError
from ooju.core.codegen import generate


def _line_text_from_source(code: str, line_number: int) -> str:
    lines = code.splitlines()
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1]
    return ""


class TranspileError(Exception):
    def __init__(
        self,
        line_number: int,
        message: str,
        line_text: str = "",
        filename: str = "",
        col: int | None = None,
    ):
        super().__init__(f"Line {line_number}: {message}")
        self.line_number = line_number
        self.message = message
        self.line_text = line_text
        self.filename = filename
        self.col = col

    def format_error(self) -> str:
        parts = ["", "oi! bhul ase:"]
        if self.filename:
            parts.append(f"  file    : {self.filename}")
        parts.append(f"  line    : {self.line_number}")
        if self.line_text:
            parts.append(f"  code    : {self.line_text.strip()}")
        parts.append(f"  kiba nai: {self.message}")
        parts.append("")
        return "\n".join(parts)


def transpile(code: str, filename: str = "", collect_errors: bool = False) -> tuple[str, dict]:
    try:
        tokens = tokenize(code, filename)
    except TokenizeError as e:
        line_text = e.line_text or _line_text_from_source(code, e.line)
        raise TranspileError(e.line, e.message, line_text, filename, col=e.col) from e

    try:
        ast = parse(tokens, filename, collect_errors=collect_errors)
    except ParseError as e:
        line_text = e.line_text or _line_text_from_source(code, e.line)
        raise TranspileError(e.line, e.message, line_text, filename) from e

    py_code, sourcemap = generate(ast)
    return py_code + "\n", sourcemap
