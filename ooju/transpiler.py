import re


VARIABLE_PREFIX = "dhora "
PRINT_PREFIX = "kua("
ELIF_PREFIX = "nohole jodi "
ELSE_KEYWORD = "nohole ba:"
DO_WHILE_START = "bare bare kora:"
LINE_COMMENT_PREFIX = "//"
BLOCK_COMMENT_MARKER = "///"
ELIF_ALIASES = ("nohole jodi ", "nahole jodi ")
KEYWORD_PREFIXES = (
    "dhora ",
    "kua(",
    "jodi ",
    "nohole jodi ",
    "nahole jodi ",
    "nohole ba",
    "bare bare kora",
    "jetialoike ",
)

IF_COMPARE_RE = re.compile(
    r"jodi\s+(.+?)\s+(.+?)t\s+koi\s+(besi|kom)\s+hoi,\s*tetia:"
)
IF_EQUALS_RE = re.compile(r"jodi\s+(.+?)\s+(.+?)\s+xoman\s+hoi,\s*tetia:")
IF_CONDITION_RE = re.compile(r"jodi\s+\((.*?)\)\s+hoi,\s*tetia:")
ELIF_COMPARE_RE = re.compile(
    r"(?:nohole|nahole)\s+jodi\s+(.+?)\s+(.+?)t\s+koi\s+(besi|kom)\s+hoi,\s*tetia:"
)
ELIF_EQUALS_RE = re.compile(
    r"(?:nohole|nahole)\s+jodi\s+(.+?)\s+(.+?)\s+xoman\s+hoi,\s*tetia:"
)
ELIF_CONDITION_RE = re.compile(r"(?:nohole|nahole)\s+jodi\s+\((.*?)\)\s+hoi,\s*tetia:")
FOR_LOOP_RE = re.compile(r"(.+?)\s+bar\s+bare\s+bare\s+kora:")
WHILE_LOOP_RE = re.compile(r"jetialoike\s+\((.*?)\)\s+bare\s+bare\s+kora:")
DO_WHILE_END_RE = re.compile(r"jetialoike\s+\((.*?)\)$")


class TranspileError(Exception):
    def __init__(self, line_number: int, message: str):
        super().__init__(f"Line {line_number}: {message}")
        self.line_number = line_number
        self.message = message


def _raise_syntax_error(line_number: int, message: str) -> None:
    raise TranspileError(line_number, message)


def _translate_comparison(prefix: str, left: str, right: str, relation: str) -> str:
    op = ">" if relation == "besi" else "<"
    return f"{prefix} {left.strip()} {op} {right.strip()}:"


def _translate_equals(prefix: str, left: str, right: str) -> str:
    return f"{prefix} {left.strip()} == {right.strip()}:"


def _split_inline_comment(line: str) -> tuple[str, str]:
    in_single_quote = False
    in_double_quote = False
    escaped = False

    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            continue

        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            continue

        if not in_single_quote and not in_double_quote and line[index : index + 2] == LINE_COMMENT_PREFIX:
            return line[:index], line[index + 2 :].strip()

    return line.rstrip(), ""


def transpile(code: str) -> str:
    lines = code.splitlines()
    new_lines = []
    do_while_stack = []
    block_comment_start = None

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        code_part, inline_comment = _split_inline_comment(line)
        stripped_code = code_part.strip()
        indent = len(code_part) - len(code_part.lstrip(" "))
        indent_str = " " * indent

        if "\t" in line[: len(line) - len(line.lstrip())]:
            _raise_syntax_error(line_number, "tabs are not supported for indentation; use spaces")

        if not stripped:
            new_lines.append("")
            continue

        if stripped == BLOCK_COMMENT_MARKER:
            if block_comment_start is None:
                block_comment_start = line_number
            else:
                block_comment_start = None
            new_lines.append("")
            continue

        if block_comment_start is not None:
            new_lines.append("")
            continue

        if stripped.startswith(BLOCK_COMMENT_MARKER):
            new_lines.append(indent_str + "#" + stripped[3:])
            continue

        if stripped.startswith(LINE_COMMENT_PREFIX):
            new_lines.append(indent_str + "#" + stripped[2:])
            continue

        if stripped.startswith("#"):
            new_lines.append(line)
            continue

        if not stripped_code:
            new_lines.append("")
            continue

        if stripped_code == "dhora" or stripped_code.startswith(VARIABLE_PREFIX):
            assignment = stripped_code[len("dhora"):].strip()
            if not assignment:
                _raise_syntax_error(line_number, "missing variable assignment after 'dhora'")
            transpiled_line = indent_str + assignment
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        if stripped_code.startswith(PRINT_PREFIX):
            if not stripped_code.endswith(")"):
                _raise_syntax_error(line_number, "invalid kua(...) statement")
            transpiled_line = indent_str + "print" + stripped_code[3:]
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_if = IF_COMPARE_RE.fullmatch(stripped_code)
        if match_if:
            transpiled_line = (
                indent_str
                + _translate_comparison(
                    "if", match_if.group(1), match_if.group(2), match_if.group(3)
                )
            )
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_xoman = IF_EQUALS_RE.fullmatch(stripped_code)
        if match_xoman:
            transpiled_line = (
                indent_str + _translate_equals("if", match_xoman.group(1), match_xoman.group(2))
            )
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_if_condition = IF_CONDITION_RE.fullmatch(stripped_code)
        if match_if_condition:
            transpiled_line = indent_str + f"if {match_if_condition.group(1).strip()}:"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_elif = ELIF_COMPARE_RE.fullmatch(stripped_code)
        if match_elif:
            transpiled_line = (
                indent_str
                + _translate_comparison(
                    "elif", match_elif.group(1), match_elif.group(2), match_elif.group(3)
                )
            )
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_elif_xoman = ELIF_EQUALS_RE.fullmatch(stripped_code)
        if match_elif_xoman:
            transpiled_line = (
                indent_str
                + _translate_equals("elif", match_elif_xoman.group(1), match_elif_xoman.group(2))
            )
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_elif_condition = ELIF_CONDITION_RE.fullmatch(stripped_code)
        if match_elif_condition:
            transpiled_line = indent_str + f"elif {match_elif_condition.group(1).strip()}:"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        if stripped_code == ELSE_KEYWORD:
            transpiled_line = indent_str + "else:"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_for = FOR_LOOP_RE.fullmatch(stripped_code)
        if match_for:
            count_expr = match_for.group(1).strip()
            transpiled_line = indent_str + f"for _ in range({count_expr}):"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_while = WHILE_LOOP_RE.fullmatch(stripped_code)
        if match_while:
            transpiled_line = indent_str + f"while {match_while.group(1).strip()}:"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        if stripped_code == DO_WHILE_START:
            do_while_stack.append(line_number)
            transpiled_line = indent_str + "while True:"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        match_dowhile_end = DO_WHILE_END_RE.fullmatch(stripped_code)
        if match_dowhile_end:
            if not do_while_stack:
                _raise_syntax_error(
                    line_number,
                    "found 'jetialoike (...)' do-while terminator without a matching 'bare bare kora:'",
                )
            do_while_stack.pop()
            condition = match_dowhile_end.group(1).strip()
            transpiled_line = indent_str + f"if not ({condition}): break"
            if inline_comment:
                transpiled_line += f"  # {inline_comment}"
            new_lines.append(transpiled_line)
            continue

        if stripped_code.startswith(KEYWORD_PREFIXES):
            _raise_syntax_error(line_number, f"could not understand Ooju syntax: {stripped_code}")

        transpiled_line = code_part.rstrip()
        if inline_comment:
            transpiled_line += f"  # {inline_comment}"
        new_lines.append(transpiled_line)

    if do_while_stack:
        _raise_syntax_error(
            do_while_stack[-1],
            "do-while block is missing a closing 'jetialoike (...)' condition",
        )

    if block_comment_start is not None:
        _raise_syntax_error(
            block_comment_start,
            "block comment opened with '///' is missing a closing '///'",
        )

    return "\n".join(new_lines) + ("\n" if code.endswith("\n") else "")
