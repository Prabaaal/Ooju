import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from ooju.cli.main import main
from ooju.cli.repl import run_repl


class CliTests(unittest.TestCase):
    def test_runs_oj_file_directly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            program = Path(tmp_dir) / "hello.oj"
            program.write_text('kua("Namaskar")\n', encoding="utf-8")

            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main([str(program)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout_buffer.getvalue(), "Namaskar\n")
        self.assertEqual(stderr_buffer.getvalue(), "")

    def test_compile_command_writes_python_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            program = Path(tmp_dir) / "hello.oj"
            program.write_text('kua("Namaskar")\n', encoding="utf-8")

            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(["compile", str(program)])

            compiled_path = Path(stdout_buffer.getvalue().strip())
            self.assertEqual(exit_code, 0)
            self.assertTrue(compiled_path.exists())
            self.assertIn('print("Namaskar")', compiled_path.read_text(encoding="utf-8"))
            self.assertEqual(stderr_buffer.getvalue(), "")

    def test_debug_mode_prints_transpiled_python_to_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            program = Path(tmp_dir) / "hello.oj"
            program.write_text('kua("Namaskar")\n', encoding="utf-8")

            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(["run", str(program), "--debug"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout_buffer.getvalue(), "Namaskar\n")
        self.assertIn("Transpiled Python:", stderr_buffer.getvalue())
        self.assertIn('print("Namaskar")', stderr_buffer.getvalue())

    def test_version_command_prints_version(self) -> None:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main(["version"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr_buffer.getvalue(), "")
        self.assertIn("1.0.1", stdout_buffer.getvalue())

    def test_rejects_non_oj_files(self) -> None:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main(["run", "notes.txt"])

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout_buffer.getvalue(), "")
        self.assertIn("expected a .oj source file", stderr_buffer.getvalue())

    def test_returns_error_for_missing_file(self) -> None:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main(["run", "missing.oj"])

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout_buffer.getvalue(), "")
        self.assertIn("file not found", stderr_buffer.getvalue())

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

    def test_run_command_rejects_python_builtin_escape_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            program = Path(tmp_dir) / "escape.oj"
            program.write_text('kua(__import__("os").getcwd())\n', encoding="utf-8")

            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(["run", str(program)])

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout_buffer.getvalue(), "")
        self.assertIn("ki bhul hoise", stderr_buffer.getvalue().lower())

    def test_repl_rejects_python_builtin_escape_payload(self) -> None:
        stdout_buffer = io.StringIO()
        with patch("builtins.input", side_effect=['kua(__import__("os").getcwd())', "jau"]):
            with redirect_stdout(stdout_buffer):
                run_repl()

        output = stdout_buffer.getvalue().lower()
        self.assertNotIn("/users/", output)
        self.assertIn("valid nohoi", output)


if __name__ == "__main__":
    unittest.main()
