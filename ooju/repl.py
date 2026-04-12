import sys
from ooju.tokenizer import tokenize, TokenizeError
from ooju.parser import parse, ParseError, MultiParseError
from ooju.codegen import generate
from ooju.transpiler import TranspileError

BANNER = """
┌─────────────────────────────────┐
│  Ooju REPL  v1.0.0              │
│  bahir hobole: 'jau' or Ctrl+C  │
└─────────────────────────────────┘
"""

REPL_KEYWORDS = ("jau", "exit", "quit", "oba")


def run_repl():
    print(BANNER)
    session_globals = {"__name__": "__main__"}
    buffer = []
    indent_expected = False

    while True:
        try:
            prompt = "... " if buffer else "ooju> "
            try:
                import readline
            except ImportError:
                pass
            line = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nBye! Akou ahiba 👋")
            break

        if not buffer and line.strip() in REPL_KEYWORDS:
            print("Bye! Akou ahiba 👋")
            break

        # empty line = end of indented block
        if line.strip() == "" and buffer:
            full_code = "\n".join(buffer)
            buffer = []
            indent_expected = False
            _execute(full_code, session_globals)
            continue

        if line.strip() == "":
            continue

        buffer.append(line)

        # if line ends with ':', next line is indented block
        if line.rstrip().endswith(":"):
            indent_expected = True
            continue

        # if we're not in a block, execute immediately
        if not indent_expected:
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
