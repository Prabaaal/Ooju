# Beginner Diagnostics Design

Date: 2026-05-01
Project: Ooju
Topic: Beginner-first syntax diagnostics in romanized Assamese

## Summary

Ooju's next beginner-first improvement should be a structured diagnostics system that teaches users how to fix the exact line they just broke. The first phase should focus on tokenizer, parser, and syntax-checking failures. All beginner-facing output should default to romanized Assamese so the language feels consistent and teachable from the CLI now and from the future playground later.

This feature is not about adding new syntax. It is about making the current language easier to learn when mistakes happen.

## Goals

- Show beginners exactly where the error happened.
- Explain what Ooju expected in simple romanized Assamese.
- Suggest one or two direct fixes instead of only reporting failure.
- Keep error output consistent across `ooju check` and `ooju run`.
- Build a reusable diagnostics layer that the future playground website can consume.

## Non-Goals

- Adding new language syntax or runtime features.
- Solving advanced runtime error teaching in the first phase.
- Building the playground UI in this project phase.
- Translating internal implementation details into multiple human languages in the first phase.

## Problem

The current error flow already captures useful low-level information such as line numbers, code text, and raw parser or tokenizer messages. However, the final CLI output is still too close to internal compiler phrasing. A beginner may see where the failure happened without clearly understanding:

- ki bhul hoise
- kio hoise
- etiya ki kori line-tu thik kora jai

This creates a teaching gap. Ooju already knows enough context to be more helpful, but it does not yet convert that context into a consistent beginner-facing diagnostic format.

## User Experience Direction

All beginner-facing diagnostics should use romanized Assamese by default.

The tone should be:

- simple
- repetitive in structure
- direct
- calm, not sarcastic
- focused on helping the learner fix the current line

The wording does not need to be perfect in this phase. Message text should be easy to revise manually later without changing the diagnostics architecture.

## Proposed Approach

Introduce a dedicated diagnostics layer between core compiler errors and CLI rendering.

### Layer 1: Core Error Sources

Tokenizer and parser code should continue to raise precise low-level errors with structured context such as:

- line
- optional column
- code snippet or original line text
- internal message
- optional filename
- optional internal error code

These errors should remain implementation-focused and not be overloaded with long end-user teaching text.

### Layer 2: Diagnostic Builder

Add a new module responsible for converting low-level errors into a structured beginner-facing diagnostic object.

Suggested fields:

- `code`: stable internal identifier such as `missing_assign_after_dhora`
- `title`: short romanized Assamese summary
- `line`: source line number
- `column`: optional source column
- `snippet`: source line text
- `pointer`: optional caret or token highlight data
- `problem`: short statement of what failed
- `bujha`: simple explanation of why Ooju rejected it
- `thik_kora`: one or two concrete fixes
- `udaharan`: optional corrected example
- `filename`: optional source path

The builder should map known parser or tokenizer messages into stable teaching diagnostics. Unknown failures should fall back to a generic romanized Assamese diagnostic template instead of leaking raw Python or English-heavy internal output.

### Layer 3: CLI Renderer

The CLI should render diagnostics consistently for:

- `ooju check`
- `ooju run` when syntax fails
- future runtime teaching flow

Suggested output shape:

1. Short title
2. File and line
3. Code snippet
4. Optional pointer
5. `bujha`
6. `thik_kora`
7. `udaharan` when helpful

This keeps the teaching model stable even if later surfaces such as the website render the same diagnostic data differently.

## Why This Approach

This approach is recommended over embedding beginner text directly inside parser or tokenizer errors because:

- it keeps compiler internals small and focused
- it allows message wording to evolve without changing parsing logic
- it gives the playground a reusable structured format later
- it supports consistent romanized Assamese output everywhere
- it makes testing easier because diagnostics can be asserted independently from parsing behavior

## Alternatives Considered

### Option 1: Improve Existing `format_error()` Strings Only

This would be the smallest implementation. It would speed up initial output improvements but would mix teaching logic into current error classes and make future UI reuse harder.

Tradeoff:

- good for a quick patch
- weak for long-term reuse and consistency

### Option 2: Full Syntax And Runtime Diagnostic System Immediately

This would create the best end-to-end learner experience faster, but it expands scope too early and risks delaying the first real beginner improvement.

Tradeoff:

- strongest long-term vision
- too much surface area for the first phase

### Recommended Option: Staged Full Stack

Start with syntax diagnostics architecture now, then extend the same model to runtime errors after the syntax flow is stable.

Tradeoff:

- slightly delayed runtime teaching
- best balance of impact, scope, and future reuse

## Phase 1 Scope

Phase 1 should cover tokenizer, parser, and syntax-checking failures only.

Priority error categories:

- missing `=` after `dhora`
- malformed `jodi ... tetia`
- malformed `nohole jodi`
- missing `:` at block openers
- invalid indentation shape
- unexpected token at statement start
- incomplete function declaration
- unclosed string
- invalid character or unknown token
- block termination mismatches for supported block styles

Each category should have a specific diagnostic mapping when possible.

## Phase 1 Output Rules

- Default language is romanized Assamese.
- Avoid mixed English teaching text except when quoting literal syntax like `dhora`, `=`, or `:`.
- Use short sentences.
- Prefer one fix at a time over long advice lists.
- Keep the format repeatable across all syntax failures.
- Unknown errors should still be rendered in the same template with simpler fallback text.

## Error Data Flow

1. Source file is read by the CLI.
2. Tokenizer or parser raises a low-level error.
3. The diagnostics layer converts that error into a structured diagnostic object.
4. The CLI renders the diagnostic in romanized Assamese.
5. The command exits with failure without showing unrelated internal traces.

## Runtime Extension Plan

Runtime teaching should be Phase 2, not Phase 1.

Reason:

- the CLI already has source-map support for mapping executed Python lines back to Ooju lines
- syntax errors are more common for beginners
- syntax diagnostics should establish the teaching model first

Phase 2 should reuse the same diagnostic object structure for selected runtime mistakes such as:

- undefined variable usage
- wrong function call shape
- invalid list or dict access
- type-mismatch style beginner mistakes

## Testing Strategy

Tests should verify both behavior and teaching output.

Add tests for:

- known parser or tokenizer failures mapping to the correct diagnostic code
- romanized Assamese rendering shape
- presence of line, snippet, and fix suggestions
- fallback rendering for unknown failures
- CLI consistency between `check` and `run` on syntax errors

Testing should avoid hard-coding every sentence too rigidly if message wording is expected to evolve. Stable assertions should focus on:

- diagnostic code
- key sections
- presence of expected snippet and suggested fix tokens

## Risks

### Risk: Message Wording Feels Unnatural

This is acceptable in the first implementation as long as the structure is solid and wording is easy to edit later.

Mitigation:

- keep wording centralized in the diagnostics layer

### Risk: Too Much Parser Knowledge Leaks Into The Mapping Layer

Mitigation:

- use stable error identifiers where practical instead of matching only free-form strings

### Risk: Scope Creep Into Runtime Teaching

Mitigation:

- explicitly stop Phase 1 at syntax diagnostics and check flow consistency

## Implementation Boundaries

This design likely affects:

- CLI error handling
- transpiler error conversion
- parser and tokenizer error metadata
- new diagnostics module
- test suite

This design does not require:

- changing the language grammar
- changing the VS Code extension first
- building the website playground now

## Success Criteria

This project is successful when:

- a beginner can see the exact broken line
- the output explains the likely mistake in romanized Assamese
- the output suggests a direct next fix
- `ooju check` and syntax-failure paths in `ooju run` feel consistent
- the implementation produces structured data that can later be reused in the playground

## Recommended Next Step

After this spec is approved, the next step should be a detailed implementation plan for the staged beginner diagnostics system, starting with syntax diagnostics and a reusable renderer.
