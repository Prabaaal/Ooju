from ooju.core.tokenizer import tokenize, TokenizeError
from ooju.core.parser import parse, ParseError, MultiParseError
from ooju.core.codegen import generate


class TranspileError(Exception):
    def __init__(self, line_number: int, message: str, line_text: str = "", filename: str = ""):
        super().__init__(f"Line {line_number}: {message}")
        self.line_number = line_number
        self.message = message
        self.line_text = line_text
        self.filename = filename

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
        raise TranspileError(e.line, e.message, e.line_text, filename) from e

    try:
        ast = parse(tokens, filename, collect_errors=collect_errors)
    except ParseError as e:
        raise TranspileError(e.line, e.message, e.line_text, filename) from e

    py_code, sourcemap = generate(ast)
    return py_code + "\n", sourcemap
