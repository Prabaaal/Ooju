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
