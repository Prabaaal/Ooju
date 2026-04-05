# Changelog

All notable changes to this project will be documented in this file.

## 2026-04-06

### Fixed
- Improved Ooju transpiler comment parsing for `//` and `///` edge cases.
- Fixed inline triple-slash comments so they transpile to clean Python comments.
- Preserved indentation for comment-only lines to avoid malformed output in nested blocks.

### Tests
- Added regression coverage for triple-slash comment translation and indented comment handling.
- Verified the full test suite passes with 137 tests green.
