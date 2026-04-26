import sys
from ooju.core.tokenizer import tokenize, TokenizeError, TT
from ooju.core.parser import parse, ParseError, MultiParseError
from ooju.core.codegen import generate
from ooju.core.transpiler import TranspileError

BANNER = """
┌─────────────────────────────────┐
│  Ooju REPL  v1.0.0              │
│  bahir hobole: 'jau' or Ctrl+C  │
└─────────────────────────────────┘
"""

REPL_KEYWORDS = ("jau", "exit", "quit", "oba")


def _is_complete(code: str) -> bool:
    """Return True if `code` is a syntactically complete Ooju program.

    Uses the tokenizer to count INDENT/DEDENT depth rather than scanning for
    a raw ':' character — the old approach broke for ':' inside strings and
    for brace-style blocks.  (Phase 4 fix)
    """
    try:
        tokens = tokenize(code, "<repl>")
        depth = 0
        for t in tokens:
            if t.type == TT.INDENT:
                depth += 1
            elif t.type == TT.DEDENT:
                depth -= 1
        return depth == 0
    except TokenizeError:
        # Tokenize error may mean incomplete input — keep buffering
        return False


def run_repl():
    print(BANNER)
    session_globals = {"__name__": "__main__"}
    buffer: list[str] = []

    while True:
        try:
            prompt = "... " if buffer else "ooju> "
            try:
                import readline  # noqa: F401 — enables line editing on Unix
            except ImportError:
                pass
            line = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nBye! Akou ahiba 👋")
            break

        if not buffer and line.strip() in REPL_KEYWORDS:
            print("Bye! Akou ahiba 👋")
            break

        # Empty line while buffering = user signals end of block
        if line.strip() == "" and buffer:
            full_code = "\n".join(buffer)
            buffer = []
            _execute(full_code, session_globals)
            continue

        if line.strip() == "":
            continue

        buffer.append(line)

        # Use tokenizer-based completeness check (FIXED: was raw endswith(":"))
        if _is_complete("\n".join(buffer)):
            full_code = "\n".join(buffer)
            buffer = []
            _execute(full_code, session_globals)


def _execute(code: str, session_globals: dict):
    try:
        tokens = tokenize(code, "<repl>")
        ast = parse(tokens, "<repl>")
        py_code, sourcemap = generate(ast)
        compiled = compile(py_code, "<repl>", "exec")
        exec(compiled, session_globals)
    except TokenizeError as e:
        print(e.format_error())
    except MultiParseError as e:
        print(e.format_error())
    except ParseError as e:
        print(e.format_error())
    except TranspileError as e:
        print(e.format_error())
    except SyntaxError as e:
        print(f"\noi! bhul ase:\n  kiba nai: {e.msg} (line {e.lineno})\n")
    except Exception as e:
        print(f"\noi! runtime-t bhul:\n  kiba nai: {e}\n")
