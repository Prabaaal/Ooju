import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from ooju.cli import main


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
        self.assertIn("1.0.0", stdout_buffer.getvalue())

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


if __name__ == "__main__":
    unittest.main()
