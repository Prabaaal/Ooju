# 🌿 Ooju
> *"Programming, made easy in Assamese"*

Ooju (উজু) is a beginner-friendly programming language that uses Assamese-inspired keywords and transpiles to Python. Version `1.0.0` upgrades the project from a regex-only prototype into a tokenizer + parser + code generator pipeline with friendlier errors, stronger CLI tooling, and a more complete teaching-friendly syntax.

## Quick Start
```bash
pip install .
```

Create an Ooju program:

```ooju
kaam greet(name):
    kua("Namaskar, " + name)

dhora naam = lobo("Tomar naam ki? ")
greet(naam)
```

Run it:

```bash
ooju run hello.oj
```

See the generated Python:

```bash
ooju run hello.oj --debug
```

Compile to a Python file:

```bash
ooju compile hello.oj
```

Other commands:

```bash
ooju version
ooju help
```

## Language Notes
`dhora x = 5` creates or updates a variable.
`kua(...)` prints values.
`lobo(...)` maps to Python's `input(...)`.
`kaam add(a, b):` defines a function.
`return value` works inside functions.
`[1, 2, 3]`, dictionaries, slices, and most Python-style expressions are preserved.
`jodi (condition) hoi, tetia:` works like `if condition:`.
`nohole jodi ...` and `nahole jodi ...` work like `elif`.
`nohole ba:` works like `else:`.
`3 bar kora:` and `3 bar bare bare kora:` both repeat a block.
`jetialoike (condition) bare bare kora:` works like a `while` loop.
`bare bare kora:` followed by `jetialoike (condition)` works like a do-while loop.
`//` starts a single-line or inline comment.
Wrap ignored lines between `///` and `///` for a block comment.
Use spaces for indentation. Tabs are rejected with a formatted `OojuError`.

## Error Style
Transpile errors now include the file, line, source code, issue, and a suggestion when available. Example:

```text
OojuError:
  File : hello.oj
  Line : 3
  Code : dhora naam
  Issue: missing assignment after 'dhora'
  Help : Did you mean: dhora x = 10 ?
```

## Runtime Safety
Ooju programs execute with a small safe builtins set instead of the full Python builtins namespace. Common helpers like `print`, `input`, `len`, `sum`, `range`, `min`, `max`, `int`, `float`, `str`, `list`, and `dict` are available by default.

## Architecture
The transpiler now follows three stages:

1. Tokenizer
2. Parser that builds statement nodes such as assignments, functions, loops, and conditionals
3. Code generator that emits Python

This keeps the language easier to grow while preserving the current lightweight feel.

## Examples
Check the `examples/` folder for:

`hello.oj` for the simplest run.
`fibonacci.oj` for a function-based demo.
`chat_test.oj` for a small branching conversation flow.
`number_report.oj` for loops and conditions together.

## Editor Support
Syntax highlighting for `.oj` files is available in the local VS Code extension at `editors/vscode`.
