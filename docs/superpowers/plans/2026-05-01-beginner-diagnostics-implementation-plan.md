# Beginner Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable beginner diagnostics system for Ooju syntax failures that renders consistent romanized Assamese help in `ooju check` and `ooju run`.

**Architecture:** Keep tokenizer and parser errors low-level, add a new diagnostics translator module in `ooju/core/`, and route CLI syntax failures through a single renderer. Phase 1 stops at tokenizer/parser/check flows, but the data shape should be reusable for future runtime diagnostics.

**Tech Stack:** Python 3, `unittest`, existing Ooju tokenizer/parser/transpiler/CLI modules

---

## File Structure

### New files

- `ooju/core/diagnostics.py`
  Responsibility: define the diagnostic dataclass, map low-level tokenizer/parser/transpiler failures into stable diagnostic codes, and render a consistent romanized Assamese output block for the CLI.

- `tests/test_diagnostics.py`
  Responsibility: focused unit tests for diagnostic mapping and renderer behavior without needing to exercise the whole CLI every time.

### Existing files to modify

- `ooju/core/tokenizer.py`
  Responsibility: preserve and expose the metadata the diagnostics layer needs, especially `col`, `line_text`, and stable error messages for common beginner failures.

- `ooju/core/parser.py`
  Responsibility: preserve and expose parse failure context consistently, and optionally tighten a few common error messages so they map cleanly to stable diagnostic codes.

- `ooju/core/transpiler.py`
  Responsibility: carry low-level error metadata forward in `TranspileError` so the diagnostics layer can consume one normalized error object.

- `ooju/cli/main.py`
  Responsibility: replace direct `format_error()` output for syntax failures with rendering from the new diagnostics layer in `check` and `run`.

- `tests/test_cli.py`
  Responsibility: assert that CLI syntax errors use the new romanized Assamese rendering shape in both commands.

- `tests/test_transpiler.py`
  Responsibility: adjust assertions that currently lock onto old error formatting if they conflict with the new normalized diagnostic flow.

## Task 1: Add the Diagnostics Core

**Files:**
- Create: `ooju/core/diagnostics.py`
- Test: `tests/test_diagnostics.py`

- [ ] **Step 1: Write the failing diagnostic mapping tests**

```python
import unittest

from ooju.core.diagnostics import build_diagnostic
from ooju.core.transpiler import TranspileError


class DiagnosticMappingTests(unittest.TestCase):
    def test_maps_missing_assign_after_dhora(self) -> None:
        err = TranspileError(
            1,
            "'dhora naam' ৰ পিছত '=' lage",
            line_text="dhora naam",
            filename="demo.oj",
        )

        diagnostic = build_diagnostic(err)

        self.assertEqual(diagnostic.code, "missing_assign_after_dhora")
        self.assertEqual(diagnostic.line, 1)
        self.assertIn("dhora naam", diagnostic.snippet)
        self.assertIn("=", " ".join(diagnostic.thik_kora))
        self.assertIn("dhora", diagnostic.title)

    def test_unknown_messages_fall_back_to_generic_diagnostic(self) -> None:
        err = TranspileError(3, "ajina bhul", line_text="kua(", filename="demo.oj")

        diagnostic = build_diagnostic(err)

        self.assertEqual(diagnostic.code, "generic_syntax_error")
        self.assertIn("ki bhul hoise", diagnostic.problem.lower())
        self.assertGreaterEqual(len(diagnostic.thik_kora), 1)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_diagnostics.py -v`
Expected: FAIL with `ModuleNotFoundError` or import failure for `ooju.core.diagnostics`

- [ ] **Step 3: Write the minimal diagnostics module**

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Diagnostic:
    code: str
    title: str
    line: int
    column: int | None
    snippet: str
    problem: str
    bujha: str
    thik_kora: list[str]
    udaharan: str | None = None
    filename: str = ""


def build_diagnostic(error) -> Diagnostic:
    message = getattr(error, "message", str(error))
    line = getattr(error, "line_number", getattr(error, "line", 0))
    column = getattr(error, "col", None)
    snippet = getattr(error, "line_text", "") or ""
    filename = getattr(error, "filename", "") or ""

    if message.startswith("'dhora ") and "' ৰ পিছত '=' lage" in message:
        return Diagnostic(
            code="missing_assign_after_dhora",
            title="`dhora` line-tu adha thaki gol",
            line=line,
            column=column,
            snippet=snippet,
            problem="Variable bonabo bisarisa, kintu value dibole `=` nai.",
            bujha="Ooju-t `dhora` use korile variable name-r pisot `=` aru ekta value thakibo lage.",
            thik_kora=[
                "`dhora naam = \"Prabal\"` nisina likha.",
                "Jodi value etiya najana, tobu `=`-r pisot kisu value diya.",
            ],
            udaharan="dhora naam = \"Prabal\"",
            filename=filename,
        )

    return Diagnostic(
        code="generic_syntax_error",
        title="syntax line-t kisu golmal ase",
        line=line,
        column=column,
        snippet=snippet,
        problem="Ki bhul hoise, Ooju-e etiya ei line-tu bujhi pua nai.",
        bujha="Ei line-t syntax rule-r logot mil nai, karone parse nohoi.",
        thik_kora=[
            "Line-tu aru ebar bhalke saa.",
            "Bracket, colon, aru keyword order thik ase niki check kora.",
        ],
        udaharan=None,
        filename=filename,
    )
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_diagnostics.py -v`
Expected: PASS for both diagnostic mapping tests

- [ ] **Step 5: Commit**

```bash
git add ooju/core/diagnostics.py tests/test_diagnostics.py
git commit -m "feat: add beginner diagnostics core"
```

## Task 2: Add a Stable CLI Renderer

**Files:**
- Modify: `ooju/core/diagnostics.py`
- Test: `tests/test_diagnostics.py`

- [ ] **Step 1: Write the failing renderer test**

```python
def test_renderer_uses_romanized_assamese_sections(self) -> None:
    err = TranspileError(
        1,
        "'dhora naam' ৰ পিছত '=' lage",
        line_text="dhora naam",
        filename="demo.oj",
    )

    diagnostic = build_diagnostic(err)
    rendered = render_diagnostic(diagnostic)

    self.assertIn("ki bhul hoise", rendered.lower())
    self.assertIn("bujha", rendered.lower())
    self.assertIn("thik kora", rendered.lower())
    self.assertIn("demo.oj", rendered)
    self.assertIn("dhora naam", rendered)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_diagnostics.py::DiagnosticMappingTests::test_renderer_uses_romanized_assamese_sections -v`
Expected: FAIL with `NameError` or import failure for `render_diagnostic`

- [ ] **Step 3: Add the renderer to `ooju/core/diagnostics.py`**

```python
def render_diagnostic(diagnostic: Diagnostic) -> str:
    parts = [""]
    parts.append(f"oi! {diagnostic.title}")

    if diagnostic.filename:
        parts.append(f"file: {diagnostic.filename}")
    parts.append(f"line: {diagnostic.line}")

    if diagnostic.snippet:
        parts.append(f"code: {diagnostic.snippet}")

    parts.append(f"ki bhul hoise: {diagnostic.problem}")
    parts.append(f"bujha: {diagnostic.bujha}")

    for index, fix in enumerate(diagnostic.thik_kora, 1):
        parts.append(f"thik kora {index}: {fix}")

    if diagnostic.udaharan:
        parts.append(f"udaharan: {diagnostic.udaharan}")

    parts.append("")
    return "\n".join(parts)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_diagnostics.py -v`
Expected: PASS, including renderer coverage

- [ ] **Step 5: Commit**

```bash
git add ooju/core/diagnostics.py tests/test_diagnostics.py
git commit -m "feat: add romanized assamese diagnostic renderer"
```

## Task 3: Route Syntax Failures Through the Diagnostics Layer

**Files:**
- Modify: `ooju/cli/main.py`
- Modify: `ooju/core/transpiler.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write the failing CLI tests**

```python
def test_check_command_renders_beginner_diagnostic_for_syntax_error(self) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        program = Path(tmp_dir) / "broken.oj"
        program.write_text("dhora naam\n", encoding="utf-8")

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main(["check", str(program)])

    self.assertEqual(exit_code, 1)
    self.assertEqual(stdout_buffer.getvalue(), "")
    self.assertIn("ki bhul hoise", stderr_buffer.getvalue().lower())
    self.assertIn("thik kora", stderr_buffer.getvalue().lower())
    self.assertIn("dhora naam", stderr_buffer.getvalue())


def test_run_command_renders_same_syntax_diagnostic_shape(self) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        program = Path(tmp_dir) / "broken.oj"
        program.write_text("dhora naam\n", encoding="utf-8")

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main(["run", str(program)])

    self.assertEqual(exit_code, 1)
    self.assertIn("ki bhul hoise", stderr_buffer.getvalue().lower())
    self.assertIn("thik kora", stderr_buffer.getvalue().lower())
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_cli.py -v`
Expected: FAIL because CLI still prints old `format_error()` output

- [ ] **Step 3: Update `ooju/core/transpiler.py` and `ooju/cli/main.py`**

```python
# ooju/core/transpiler.py
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
```

```python
# ooju/core/transpiler.py
except TokenizeError as e:
    raise TranspileError(e.line, e.message, e.line_text, filename, col=e.col) from e
```

```python
# ooju/cli/main.py
from ooju.core.diagnostics import build_diagnostic, render_diagnostic
```

```python
# ooju/cli/main.py
except MultiParseError as exc:
    for err in exc.errors:
        diagnostic = build_diagnostic(err)
        print(render_diagnostic(diagnostic), file=sys.stderr)
    return 1
except TranspileError as exc:
    diagnostic = build_diagnostic(exc)
    print(render_diagnostic(diagnostic), file=sys.stderr)
    return 1
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m pytest tests/test_cli.py -v`
Expected: PASS, with both `check` and `run` rendering beginner diagnostics for syntax failures

- [ ] **Step 5: Commit**

```bash
git add ooju/core/transpiler.py ooju/cli/main.py tests/test_cli.py
git commit -m "feat: render syntax errors through diagnostics layer"
```

## Task 4: Add Mappings for High-Value Beginner Errors

**Files:**
- Modify: `ooju/core/diagnostics.py`
- Modify: `tests/test_diagnostics.py`
- Modify: `tests/test_transpiler.py`

- [ ] **Step 1: Write the failing high-value mapping tests**

```python
def test_maps_missing_colon_after_condition(self) -> None:
    err = TranspileError(
        2,
        "condition ৰ শেষত ':' লাগে",
        line_text="jodi x > 5 tetia",
        filename="demo.oj",
    )

    diagnostic = build_diagnostic(err)

    self.assertEqual(diagnostic.code, "missing_colon_after_condition")
    self.assertIn(":", " ".join(diagnostic.thik_kora))
    self.assertIn("jodi", diagnostic.udaharan)


def test_maps_unclosed_lua_parenthesis(self) -> None:
    err = TranspileError(
        4,
        "'lua(...)' বন্ধ কৰা নাই ')'",
        line_text='dhora naam = lua("tomar naam ki?"',
        filename="demo.oj",
    )

    diagnostic = build_diagnostic(err)

    self.assertEqual(diagnostic.code, "unclosed_parenthesis")
    self.assertIn(")", " ".join(diagnostic.thik_kora))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_diagnostics.py -v`
Expected: FAIL because both messages still fall back to `generic_syntax_error`

- [ ] **Step 3: Extend `build_diagnostic()` with concrete mappings**

```python
if message == "condition ৰ শেষত ':' লাগে":
    return Diagnostic(
        code="missing_colon_after_condition",
        title="condition-r sesot colon nai",
        line=line,
        column=column,
        snippet=snippet,
        problem="Condition line sesh koribole `:` dibo lagisil.",
        bujha="`jodi ... tetia:` ba `nohole jodi ... tetia:` line-r sesot colon thakile next block bujhibole Ooju-r xubidha hoi.",
        thik_kora=[
            "Line-r sesot `:` diya.",
            "Tar pisot next line-t block start kora.",
        ],
        udaharan="jodi (x > 5) hoi, tetia:",
        filename=filename,
    )

if "বন্ধ কৰা নাই ')'" in message:
    return Diagnostic(
        code="unclosed_parenthesis",
        title="bracket bondho nohoi",
        line=line,
        column=column,
        snippet=snippet,
        problem="Open `(` use kora hoise, kintu tar matching `)` nai.",
        bujha="Function call ba expression-r majot opening bracket thakile closing bracket-o thakibo lage.",
        thik_kora=[
            "Sesot ekta `)` diya.",
            "Bracket count ebar milai saa.",
        ],
        udaharan='dhora naam = lua("tomar naam ki?")',
        filename=filename,
    )
```

- [ ] **Step 4: Add one end-to-end transpiler assertion and run the focused tests**

```python
def test_formats_missing_assignment_error(self) -> None:
    with self.assertRaises(TranspileError) as ctx:
        transpile("dhora naam\n", filename="demo.oj")

    self.assertIn("'dhora naam' ৰ পিছত '=' lage", ctx.exception.message)
    self.assertEqual(ctx.exception.line_number, 1)
```

Run: `python -m pytest tests/test_diagnostics.py tests/test_transpiler.py -v`
Expected: PASS, including specific code mappings for common beginner mistakes

- [ ] **Step 5: Commit**

```bash
git add ooju/core/diagnostics.py tests/test_diagnostics.py tests/test_transpiler.py
git commit -m "feat: add targeted beginner syntax diagnostics"
```

## Task 5: Normalize Multi-Error And Fallback Output

**Files:**
- Modify: `ooju/cli/main.py`
- Modify: `ooju/core/diagnostics.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing multi-error CLI test**

```python
def test_check_command_renders_multiple_diagnostics_consistently(self) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        program = Path(tmp_dir) / "broken.oj"
        program.write_text("dhora naam\njodi x > 5 tetia\n", encoding="utf-8")

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main(["check", str(program)])

    output = stderr_buffer.getvalue().lower()
    self.assertEqual(exit_code, 1)
    self.assertGreaterEqual(output.count("ki bhul hoise"), 2)
    self.assertIn("line: 1", output)
    self.assertIn("line: 2", output)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_cli.py::CliTests::test_check_command_renders_multiple_diagnostics_consistently -v`
Expected: FAIL if output shape is inconsistent across multi-error rendering

- [ ] **Step 3: Add a helper in `ooju/cli/main.py` to print one or many diagnostics**

```python
def _print_diagnostics(errors: list[Exception]) -> None:
    for error in errors:
        diagnostic = build_diagnostic(error)
        print(render_diagnostic(diagnostic), file=sys.stderr)
```

```python
except MultiParseError as exc:
    _print_diagnostics(exc.errors)
    return 1
except TranspileError as exc:
    _print_diagnostics([exc])
    return 1
```

- [ ] **Step 4: Run the CLI and diagnostics test suite**

Run: `python -m pytest tests/test_cli.py tests/test_diagnostics.py tests/test_transpiler.py -v`
Expected: PASS for single-error, multi-error, mapping, and rendering behavior

- [ ] **Step 5: Commit**

```bash
git add ooju/cli/main.py ooju/core/diagnostics.py tests/test_cli.py
git commit -m "refactor: normalize cli diagnostic output"
```

## Task 6: Final Verification And Docs Touch-Up

**Files:**
- Modify: `README.md`
- Test: `tests/test_cli.py`
- Test: `tests/test_diagnostics.py`
- Test: `tests/test_transpiler.py`

- [ ] **Step 1: Write the failing README expectation mentally, then add the docs update**

```markdown
## Beginner-Friendly Errors

Ooju syntax errors now explain:

- kot bhul hoise
- kio bhul hoise
- ene koi thik kora jai

Example commands:

```bash
ooju check examples/hello.oj
ooju run broken.oj
```
```

- [ ] **Step 2: Update `README.md` with the new section near CLI usage**

```markdown
## Beginner-Friendly Errors

Jodi syntax line-t bhul thake, Ooju etiya romanized Assamese-t bujhai dibo:

- ki bhul hoise
- bujha
- thik kora
- udaharan

Etiya `ooju check` aru `ooju run` duita command-e ekei dhorar help dikhabo.
```

- [ ] **Step 3: Run the full test suite**

Run: `python -m pytest -v`
Expected: PASS across CLI, transpiler, diagnostics, and stress tests

- [ ] **Step 4: Smoke-test the CLI manually**

Run: `python -m ooju.cli.main check examples/hello.oj`
Expected: PASS with `sob thik ase! no syntax errors found. ✅`

Run: `python -m ooju.cli.main check /tmp/broken.oj`
Expected: FAIL with romanized Assamese sections including `ki bhul hoise`, `bujha`, and `thik kora`

- [ ] **Step 5: Commit**

```bash
git add README.md tests/test_cli.py tests/test_diagnostics.py tests/test_transpiler.py ooju/core/diagnostics.py ooju/core/transpiler.py ooju/cli/main.py
git commit -m "docs: document beginner diagnostics flow"
```

## Self-Review

### Spec coverage

- Structured diagnostic object: covered in Task 1.
- Romanized Assamese renderer: covered in Task 2.
- CLI consistency for `check` and `run`: covered in Task 3 and Task 5.
- Specific beginner-first mappings for high-value syntax errors: covered in Task 4.
- Reusable foundation for later runtime diagnostics: covered by the data shape in Tasks 1 and 2.
- Testing and docs: covered in Task 6.

No spec gaps found for Phase 1.

### Placeholder scan

Checked for `TBD`, `TODO`, vague “handle errors” style steps, and missing commands. None remain.

### Type consistency

- Diagnostic builder function name: `build_diagnostic`
- Renderer function name: `render_diagnostic`
- Dataclass name: `Diagnostic`
- Shared fields remain consistent across all tasks

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-01-beginner-diagnostics-implementation-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
