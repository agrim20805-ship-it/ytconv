"""The command refuses bad input before it downloads anything.

Every case here returns before yt-dlp or the network is touched, so the tests
pass on a machine with neither.
"""
import contextlib
import io
import tempfile
import unittest
from unittest import mock

from ytconv import cli

URL = "https://www.youtube.com/watch?v=AAAAAAAAAAA"


def run(*argv):
    """main(argv) -> (exit code, what it printed to stderr)."""
    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        try:
            code = cli.main(list(argv))
        except SystemExit as exc:      # argparse refuses some combinations itself
            code = exc.code
    return code, err.getvalue()


class InputValidation(unittest.TestCase):
    def test_nothing_to_do(self):
        code, err = run()
        self.assertEqual(code, 2)
        self.assertIn("Give exactly one of", err)

    def test_gameplay_and_every_clash(self):
        code, err = run(URL, "--gameplay", "--every", "3")
        self.assertEqual(code, 2)
        self.assertIn("not allowed with argument --gameplay", err)

    def test_source_starting_with_a_dash(self):
        code, err = run("--", "-x")
        self.assertEqual(code, 2)
        self.assertIn("not something starting with '-'", err)

    def test_every_must_be_above_zero(self):
        self.assertEqual(run(URL, "--every", "0")[0], 2)

    def test_max_frames_at_least_one(self):
        self.assertEqual(run(URL, "--max-frames", "0")[0], 2)

    def test_language_code_checked(self):
        code, err = run(URL, "--lang", "not a code!")
        self.assertEqual(code, 2)
        self.assertIn("language code", err)

    def test_results_needs_search(self):
        self.assertEqual(run(URL, "--results", "5")[0], 2)

    def test_search_needs_a_topic(self):
        self.assertEqual(run("--search", "   ")[0], 2)

    def test_search_results_limit(self):
        self.assertEqual(run("--search", "black holes", "--results", "99")[0], 2)

    def test_research_page_needs_research_md(self):
        with tempfile.TemporaryDirectory() as folder:
            code, err = run("--research-page", folder)
        self.assertEqual(code, 2)
        self.assertIn("No research.md", err)

    def test_missing_programs_are_named(self):
        with mock.patch("ytconv.cli.shutil.which", return_value=None):
            code, err = run(URL, "--no-frames")
        self.assertEqual(code, 2)
        self.assertIn("Missing program(s): yt-dlp", err)


if __name__ == "__main__":
    unittest.main()
