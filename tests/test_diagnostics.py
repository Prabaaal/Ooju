import unittest

from ooju.core.transpiler import TranspileError


class DiagnosticMappingTests(unittest.TestCase):
    def test_maps_missing_assign_after_dhora(self) -> None:
        from ooju.core.diagnostics import build_diagnostic

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
        from ooju.core.diagnostics import build_diagnostic

        err = TranspileError(3, "ajina bhul", line_text="kua(", filename="demo.oj")

        diagnostic = build_diagnostic(err)

        self.assertEqual(diagnostic.code, "generic_syntax_error")
        self.assertIn("ki bhul hoise", diagnostic.problem.lower())
        self.assertGreaterEqual(len(diagnostic.thik_kora), 1)

    def test_renderer_uses_romanized_assamese_sections(self) -> None:
        from ooju.core.diagnostics import build_diagnostic, render_diagnostic

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

    def test_maps_missing_colon_after_condition(self) -> None:
        from ooju.core.diagnostics import build_diagnostic

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
        from ooju.core.diagnostics import build_diagnostic

        err = TranspileError(
            4,
            "'lua(...)' বন্ধ কৰা নাই ')'",
            line_text='dhora naam = lua("tomar naam ki?"',
            filename="demo.oj",
        )

        diagnostic = build_diagnostic(err)

        self.assertEqual(diagnostic.code, "unclosed_parenthesis")
        self.assertIn(")", " ".join(diagnostic.thik_kora))


if __name__ == "__main__":
    unittest.main()
