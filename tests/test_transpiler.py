import unittest

from ooju.transpiler import TranspileError, transpile


class TranspilerTests(unittest.TestCase):
    def test_supports_general_if_condition_syntax(self) -> None:
        source = "\n".join(
            [
                "jodi (coin > 5) hoi, tetia:",
                '    kua("bhal")',
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("if coin > 5:", compiled)

    def test_supports_general_elif_condition_syntax(self) -> None:
        source = "\n".join(
            [
                "jodi (coin > 10) hoi, tetia:",
                '    kua("bor")',
                "nohole jodi (coin > 5) hoi, tetia:",
                '    kua("majot")',
                "nohole ba:",
                '    kua("kom")',
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("if coin > 10:", compiled)
        self.assertIn("elif coin > 5:", compiled)

    def test_supports_legacy_nahole_jodi_alias(self) -> None:
        source = "\n".join(
            [
                "jodi (coin > 10) hoi, tetia:",
                '    kua("bor")',
                "nahole jodi (coin > 5) hoi, tetia:",
                '    kua("majot")',
                "nohole ba:",
                '    kua("kom")',
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("elif coin > 5:", compiled)

    def test_supports_single_line_comments(self) -> None:
        source = "// eti comment\nkua(1)\n"

        compiled = transpile(source)

        self.assertIn("# eti comment", compiled)
        self.assertIn("print(1)", compiled)

    def test_supports_inline_comments_after_code(self) -> None:
        source = 'dhora x = 1 // eti note\nkua("http://example.com") // url thakileo thik\n'

        compiled = transpile(source)

        self.assertIn("x = 1  # eti note", compiled)
        self.assertIn('print("http://example.com")  # url thakileo thik', compiled)

    def test_supports_block_comments_delimited_by_triple_slash(self) -> None:
        source = "\n".join(
            [
                "dhora x = 1",
                "///",
                "kua(x)",
                "dhora x = 2",
                "///",
                "kua(x)",
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("x = 1", compiled)
        self.assertIn("print(x)", compiled)
        self.assertNotIn("x = 2", compiled)

    def test_supports_inline_comments_on_control_flow_lines(self) -> None:
        source = "jodi (x > 1) hoi, tetia: // branch note\n    kua(x)\n"

        compiled = transpile(source)

        self.assertIn("if x > 1:  # branch note", compiled)

    def test_rejects_unclosed_block_comments(self) -> None:
        source = "///\nkua(1)\n"

        with self.assertRaises(TranspileError) as context:
            transpile(source)

        self.assertIn("missing a closing '///'", str(context.exception))

    def test_supports_elif_style_branching(self) -> None:
        source = "\n".join(
            [
                "jodi coin 10t koi besi hoi, tetia:",
                '    kua("bor")',
                "nohole jodi coin 5t koi besi hoi, tetia:",
                '    kua("majot")',
                "nohole ba:",
                '    kua("kom")',
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("if coin > 10:", compiled)
        self.assertIn("elif coin > 5:", compiled)
        self.assertIn("else:", compiled)

    def test_do_while_requires_closing_condition(self) -> None:
        source = "bare bare kora:\n    kua(1)\n"

        with self.assertRaises(TranspileError) as context:
            transpile(source)

        self.assertIn("missing a closing", str(context.exception))

    def test_do_while_terminator_requires_matching_start(self) -> None:
        source = "jetialoike (x > 0)\n"

        with self.assertRaises(TranspileError) as context:
            transpile(source)

        self.assertIn("without a matching", str(context.exception))

    def test_transpiles_loops_and_prints(self) -> None:
        source = "\n".join(
            [
                "dhora x = 2",
                "2 bar bare bare kora:",
                "    kua(x)",
                "jetialoike (x > 0) bare bare kora:",
                "    kua(x)",
                "    dhora x = x - 1",
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("for _ in range(2):", compiled)
        self.assertIn("while x > 0:", compiled)
        self.assertIn("print(x)", compiled)

    def test_rejects_tabs_in_indentation(self) -> None:
        source = "jodi x 1t koi besi hoi, tetia:\n\tkua(x)\n"

        with self.assertRaises(TranspileError) as context:
            transpile(source)

        self.assertIn("tabs are not supported", str(context.exception))

    def test_rejects_malformed_ooju_keyword_line(self) -> None:
        source = "jodi x 1t koi besi hoi tetia:\n"

        with self.assertRaises(TranspileError) as context:
            transpile(source)

        self.assertIn("could not understand Ooju syntax", str(context.exception))

    def test_number_report_style_branching_transpiles(self) -> None:
        source = "\n".join(
            [
                "jodi (current % 2 == 0) hoi, tetia:",
                '    kua("Even")',
                "nohole jodi (current % 2 != 0) hoi, tetia:",
                '    kua("Odd")',
                "nohole ba:",
                '    kua("Impossible")',
                "",
            ]
        )

        compiled = transpile(source)

        self.assertIn("if current % 2 == 0:", compiled)
        self.assertIn("elif current % 2 != 0:", compiled)
        self.assertIn("else:", compiled)


if __name__ == "__main__":
    unittest.main()
