from __future__ import annotations

import argparse
import builtins
import sys
import traceback
from pathlib import Path
from typing import Optional, Sequence

from ooju import __version__
from ooju.transpiler import TranspileError, transpile
from ooju.parser import MultiParseError


SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in (
        "abs", "all", "any", "bool", "dict", "enumerate", "float",
        "input", "int", "len", "list", "max", "min", "print", "range",
        "round", "set", "str", "sum", "tuple",
    )
}
DEBUG_HEADER = "Transpiled Python:\n------------------"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ooju", description="Run and compile Ooju programs.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="run a .oj file")
    run_parser.add_argument("file", help="path to the .oj source file")
    run_parser.add_argument("--debug", action="store_true", help="show the transpiled Python")

    compile_parser = subparsers.add_parser("compile", help="transpile a .oj file to Python")
    compile_parser.add_argument("file", help="path to the .oj source file")
    compile_parser.add_argument(
        "-o",
        "--output",
        help="output Python file path; defaults to the same name with a .py extension",
    )
    compile_parser.add_argument("--debug", action="store_true", help="show the transpiled Python")

    check_parser = subparsers.add_parser("check", help="check syntax of a .oj file")
    check_parser.add_argument("file", help="path to the .oj source file")

    subparsers.add_parser("repl", help="start the interactive Ooju REPL")
    subparsers.add_parser("version", help="show the installed Ooju version")
    subparsers.add_parser("help", help="show this help message")
    return parser


def _normalize_argv(args: list[str]) -> list[str]:
    if not args:
        return args
    if args[0].endswith(".oj"):
        return ["run", *args]
    if args[0] == "help":
        return ["--help"]
    return args


def _validate_source_path(file_path: Path) -> None:
    if file_path.suffix != ".oj":
        raise ValueError(f"expected a .oj source file, got: {file_path}")


def _read_source(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"file not found: {file_path}") from exc
    except OSError as exc:
        raise OSError(f"could not read {file_path}: {exc}") from exc


def _print_debug(py_code: str) -> None:
    print(DEBUG_HEADER, file=sys.stderr)
    if py_code:
        print(py_code, file=sys.stderr, end="" if py_code.endswith("\n") else "\n")


def _execute_file(file_path: Path, py_code: str, sourcemap: dict) -> None:
    try:
        compiled = compile(py_code, str(file_path), "exec")
        exec_globals = {"__name__": "__main__", "__builtins__": SAFE_BUILTINS}
        exec(compiled, exec_globals)
    except Exception as exc:
        tb = exc.__traceback__
        # find the frame belonging to the executed script
        oj_line = None
        while tb:
            if tb.tb_frame.f_code.co_filename == str(file_path):
                py_line = tb.tb_lineno
                oj_line = sourcemap.get(py_line)
                break
            tb = tb.tb_next
        
        if oj_line:
            print(f"\noi! runtime bhul (Ooju line {oj_line}):\n  kiba nai: {exc}\n", file=sys.stderr)
        else:
            print(f"\noi! runtime bhul:\n  kiba nai: {exc}\n", file=sys.stderr)


def _compile_file(file_path: Path, output: Optional[str], py_code: str) -> Path:
    output_path = Path(output) if output else file_path.with_suffix(".py")
    output_path.write_text(py_code, encoding="utf-8")
    return output_path


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    parser = _build_parser()

    if not args:
        print("Usage: ooju {run,compile,check,repl,version,help} ...", file=sys.stderr)
        parser.print_help(sys.stderr)
        return 1

    if (
        len(args) == 1
        and "." in args[0]
        and args[0] not in {"run", "compile", "check", "repl", "version", "help"}
        and not args[0].startswith("-")
        and not args[0].endswith(".oj")
    ):
        print(f"Ooju runtime error: expected a .oj source file, got: {args[0]}", file=sys.stderr)
        return 1

    normalized_args = _normalize_argv(args)

    try:
        namespace = parser.parse_args(normalized_args)
    except SystemExit as exc:
        return 0 if int(exc.code) == 0 else 1

    if namespace.command == "version":
        print(__version__)
        return 0

    if namespace.command == "repl":
        from ooju.repl import run_repl
        try:
            run_repl()
        except KeyboardInterrupt:
            print("\nBye! Aahu khonja 👋")
        return 0

    if namespace.command is None:
        parser.print_help(sys.stderr)
        return 1

    if namespace.command == "check":
        file_path = Path(namespace.file)
        try:
            _validate_source_path(file_path)
            source = _read_source(file_path)
            transpile(source, filename=str(file_path), collect_errors=True)
            print("sob thik ase! no syntax errors found. ✅")
            return 0
        except MultiParseError as exc:
            print(exc.format_error(), file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"Ooju error: {exc}", file=sys.stderr)
            return 1

    if namespace.command in {"run", "compile"}:
        file_path = Path(namespace.file)
        try:
            _validate_source_path(file_path)
            source = _read_source(file_path)
            py_code, sourcemap = transpile(source, filename=str(file_path))
            
            if namespace.debug:
                _print_debug(py_code)

            if namespace.command == "run":
                _execute_file(file_path, py_code, sourcemap)
            else:
                output_path = _compile_file(file_path, namespace.output, py_code)
                print(output_path)
            return 0
        except ValueError as exc:
            print(f"Ooju runtime error: {exc}", file=sys.stderr)
            return 1
        except TranspileError as exc:
            print(exc.format_error(), file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"Ooju runtime error: {exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(
                f"Ooju runtime error in {file_path}: {exc.__class__.__name__}: {exc}",
                file=sys.stderr,
            )
            return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
