# 🌿 Ooju
> *"Programming, made easy in Assamese"*

Ooju (উজু) is a beginner-friendly programming language that uses natural Assamese keywords to lower the entry barrier into coding. Built as a Python transpiler for now, it’s designed to evolve into a standalone runtime while staying focused on accessibility, education, and community.

## Quick Start
```bash
pip install ooju
```

If you downloaded or cloned this repository locally, install it from the project folder with:

```bash
pip install .
```

Then create and run an Ooju file:

```bash
echo 'kua("Hello Ooju!")' > hello.oj
ooju run hello.oj
```

`kua(...)` is Ooju's output command. It prints exactly what you pass in, whether that is a string like `kua("Namaskar")` or a variable like `kua(x)`.

## Notes
`dhora x = 5` creates or updates a variable.
`jodi (condition) hoi, tetia:` works like `if condition:`.
`3 bar bare bare kora:` repeats a block three times.
`jetialoike (condition) bare bare kora:` works like a while loop.
`bare bare kora:` followed later by `jetialoike (condition)` works like a do-while loop.
`nohole jodi (condition) hoi, tetia:` works like `elif condition:`.
`nahole jodi ...` is still accepted as a compatibility alias.
`//` starts a single-line comment.
You can also put `//` after code on the same line.
Wrap multiple ignored lines between `///` and `///` for a block comment.
Use spaces for indentation. Tabs are rejected to avoid hard-to-debug parsing issues.

## Editor Support
Syntax highlighting for `.oj` files is available in the local VS Code extension at `editors/vscode`.
It adds Ooju language recognition, comment handling, bracket pairing, and color highlighting for keywords, strings, numbers, operators, and variables.
