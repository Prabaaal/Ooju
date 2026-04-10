import unittest

from ooju.transpiler import TranspileError, transpile


def _code(source: str) -> str:
    """Transpile and return the Python code string (ignoring the sourcemap)."""
    py, _ = transpile(source)
    return py


def _norm(s: str) -> str:
    """Collapse whitespace so assertions are space-insensitive."""
    return " ".join(s.split())


class TranspilerTests(unittest.TestCase):

    # ── basic features ──────────────────────────────────────────────

    def test_transpiles_function_definitions_and_returns(self) -> None:
        source = "kaam add(a, b):\n    return a + b\ndhora total = add(2, 3)\n"
        out = _code(source)
        self.assertIn("def add", out)
        self.assertIn("return a + b", out)
        self.assertIn("total = add", out)

    def test_translates_lua_calls(self) -> None:
        source = 'dhora naam = lua("Tomar naam ki? ")\n'
        out = _code(source)
        self.assertIn('naam = input("Tomar naam ki? ")', out)

    def test_supports_short_loop(self) -> None:
        source = "3 bar kora:\n    kua(\"loop\")\n"
        out = _code(source)
        self.assertIn("for _ in range(3):", out)

    def test_supports_long_loop(self) -> None:
        source = "3 bar bare bare kora:\n    kua(\"loop\")\n"
        out = _code(source)
        self.assertIn("for _ in range(3):", out)

    # ── if/elif/else ────────────────────────────────────────────────

    def test_supports_general_if_condition_syntax(self) -> None:
        source = "jodi (coin > 5) hoi, tetia:\n    kua(\"bhal\")\n"
        out = _code(source)
        self.assertIn("if coin > 5:", out)

    def test_supports_general_elif_condition_syntax(self) -> None:
        source = (
            "jodi (coin > 10) hoi, tetia:\n"
            '    kua("bor")\n'
            "nohole jodi (coin > 5) hoi, tetia:\n"
            '    kua("majot")\n'
            "nohole ba:\n"
            '    kua("kom")\n'
        )
        out = _code(source)
        self.assertIn("if coin > 10:", out)
        self.assertIn("elif coin > 5:", out)


    def test_supports_elif_natural_language(self) -> None:
        source = (
            "jodi coin 10t koi besi hoi, tetia:\n"
            '    kua("bor")\n'
            "nohole jodi coin 5t koi besi hoi, tetia:\n"
            '    kua("majot")\n'
            "nohole ba:\n"
            '    kua("kom")\n'
        )
        out = _code(source)
        self.assertIn("if coin > 10:", out)
        self.assertIn("elif coin > 5:", out)
        self.assertIn("else:", out)

    # ── comments ────────────────────────────────────────────────────

    def test_comments_are_stripped(self) -> None:
        """The new AST compiler strips comments entirely."""
        source = "// eti comment\nkua(1)\n"
        out = _code(source)
        self.assertNotIn("eti comment", out)
        self.assertIn("print(1)", out)

    def test_inline_comments_stripped(self) -> None:
        source = 'dhora x = 1 // eti note\nkua("http://example.com")\n'
        out = _code(source)
        self.assertNotIn("eti note", out)
        self.assertIn("x = 1", out)

    def test_block_comments_strip_content(self) -> None:
        source = "dhora x = 1\n///\nkua(x)\ndhora x = 2\n///\nkua(x)\n"
        out = _code(source)
        self.assertIn("x = 1", out)
        self.assertNotIn("x = 2", out)

    def test_control_flow_inline_comment(self) -> None:
        source = "jodi (x > 1) hoi, tetia: // branch note\n    kua(x)\n"
        out = _code(source)
        self.assertIn("if x > 1:", out)
        self.assertNotIn("branch note", out)

    # ── loops ───────────────────────────────────────────────────────

    def test_transpiles_loops_and_prints(self) -> None:
        source = (
            "dhora x = 2\n"
            "2 bar bare bare kora:\n"
            "    kua(x)\n"
            "jetialoike (x > 0) bare bare kora:\n"
            "    kua(x)\n"
            "    dhora x = x - 1\n"
        )
        out = _code(source)
        self.assertIn("for _ in range(2):", out)
        self.assertIn("while x > 0:", out)
        self.assertIn("print(x)", out)

    # ── errors ──────────────────────────────────────────────────────

    def test_rejects_tabs_in_indentation(self) -> None:
        source = "jodi x 1t koi besi hoi, tetia:\n\tkua(x)\n"
        with self.assertRaises(TranspileError) as ctx:
            transpile(source)
        self.assertIn("tab dile kaam nohoi", str(ctx.exception))

    def test_number_report_style_branching(self) -> None:
        source = (
            "jodi (current % 2 == 0) hoi, tetia:\n"
            '    kua("Even")\n'
            "nohole jodi (current % 2 != 0) hoi, tetia:\n"
            '    kua("Odd")\n'
            "nohole ba:\n"
            '    kua("Impossible")\n'
        )
        out = _code(source)
        self.assertIn("if current % 2 == 0:", out)
        self.assertIn("elif current % 2 != 0:", out)
        self.assertIn("else:", out)

    def test_formats_missing_assignment_error(self) -> None:
        with self.assertRaises(TranspileError) as ctx:
            transpile("dhora naam\n", filename="demo.oj")
        formatted = ctx.exception.format_error()
        self.assertIn("file    : demo.oj", formatted)
        self.assertIn("'dhora naam' ৰ পিছত '=' lage", formatted)

    def test_dhora_with_no_name_errors(self) -> None:
        with self.assertRaises(TranspileError):
            transpile("dhora \n")


if __name__ == "__main__":
    unittest.main()
