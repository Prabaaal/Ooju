import sys
from pathlib import Path
from typing import Optional, Sequence

from ooju.transpiler import TranspileError, transpile


USAGE = "Usage: ooju run <file.oj>"


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        print(USAGE, file=sys.stderr)
        return 1

    if len(args) == 1 and args[0].endswith(".oj"):
        file_path = Path(args[0])
    elif len(args) == 2 and args[0] == "run":
        file_path = Path(args[1])
    else:
        print(USAGE, file=sys.stderr)
        return 1

    try:
        code = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Ooju runtime error: file not found: {file_path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Ooju runtime error: could not read {file_path}: {exc}", file=sys.stderr)
        return 1

    try:
        py_code = transpile(code)
        compiled = compile(py_code, str(file_path), "exec")
        exec_globals = {"__name__": "__main__"}
        exec(compiled, exec_globals)
    except TranspileError as exc:
        print(f"Ooju transpile error in {file_path}: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Ooju runtime error in {file_path}: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
