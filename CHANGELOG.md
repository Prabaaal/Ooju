# Changelog

All notable changes to Ooju are documented here.
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

---

## [1.0.0] — 2026-04-10

### 🎉 Major Release — Full Compiler Pipeline

This release replaces the original regex-based prototype with a proper
**Tokenizer → Parser → Code Generator** architecture.

### Added
- `ooju/tokenizer.py` — full lexer producing typed tokens
- `ooju/parser.py` — AST parser covering all supported statement forms
- `ooju/codegen.py` — clean Python emitter from the AST
- `ooju/repl.py` — interactive REPL (`ooju repl`)
- `ooju/stdlib.py` — sandboxed safe builtins for runtime isolation
- `ooju compile` CLI command for producing standalone `.py` files
- Beginner-friendly `OojuError` with file, line, code, issue, and help hint
- VS Code syntax highlighting extension (`editors/vscode/`)
- Comprehensive test suite (137 tests, all passing)

### Changed
- `dhora` now handles both declaration and reassignment in one keyword
- `nohole jodi` and `nahole jodi` both accepted as `elif` equivalents
- `nohole ba` accepted as `else` equivalent
- Repeat-loop forms (`N bar kora` and `N bar bare bare kora`) unified
- Block comments (`///...///`) now fully supported at any nesting level

### Fixed
- Inline `//` comments now strip correctly without corrupting string literals
- Triple-slash block comment edge cases resolved
- Indentation preserved for comment-only lines inside nested blocks

---

## [0.1.0] — 2026-04-04

### Added
- Initial prototype using regex-based line-by-line transpilation
- Basic support for `dhora`, `kua`, `lobo`, `kaam`, `jodi/tetia/nohole ba`
- `ooju run` CLI command
- `hello.oj`, `fibonacci.oj`, `chat.oj` example programs
