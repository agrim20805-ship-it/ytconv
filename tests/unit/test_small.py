"""Small helpers: frame file names, clock times, the MCP server's argument checks,
and finding a yt-dlp that pip installed."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ytconv import fetch, frames, mcp_server, notes


class FrameNames(unittest.TestCase):
    def test_stamps(self):
        self.assertEqual(frames.seconds_to_stamp(65), "01-05")
        self.assertEqual(frames.seconds_to_stamp(3725), "01-02-05")
        self.assertEqual(frames.seconds_to_stamp(0), "00-00")
        self.assertEqual(frames.seconds_to_stamp(59.9), "00-59")


class Clock(unittest.TestCase):
    def test_clock(self):
        self.assertEqual(notes._clock(3725), "1:02:05")
        self.assertEqual(notes._clock(3599), "59:59")


class McpTimestamps(unittest.TestCase):
    def test_accepted(self):
        self.assertEqual(mcp_server._to_seconds("06:29", "at"), 389)
        self.assertEqual(mcp_server._to_seconds("1:02:05", "at"), 3725)

    def test_refused(self):
        for bad in ("6:29pm", "629", 629, "", "1:2"):
            with self.subTest(value=bad):
                with self.assertRaises(mcp_server.ToolError):
                    mcp_server._to_seconds(bad, "at")


class McpNumbers(unittest.TestCase):
    def check(self, value, kind, low, **limits):
        return mcp_server._number_arg({"n": value}, "n", kind, low, **limits)

    def test_accepted(self):
        self.assertEqual(self.check(5, int, 1), 5)
        self.assertEqual(self.check(0.5, float, 0, high=1), 0.5)
        self.assertIsNone(mcp_server._number_arg({}, "n", int, 1))

    def test_refused(self):
        cases = [(0, int, 1, {}), (True, int, 0, {}), (2.5, int, 0, {}),
                 (1.5, float, 0, {"high": 1}), (0, float, 0, {"above": True})]
        for value, kind, low, limits in cases:
            with self.subTest(value=value, kind=kind.__name__, low=low, **limits):
                with self.assertRaises(mcp_server.ToolError):
                    self.check(value, kind, low, **limits)


class PipTools(unittest.TestCase):
    """pip install "ytconv[full]" puts yt-dlp in a folder that is often not on PATH."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pip_dir = Path(self.tmp.name) / "bin"
        self.empty = Path(self.tmp.name) / "empty"
        self.pip_dir.mkdir()
        self.empty.mkdir()
        for name in ("yt-dlp", "yt-dlp.exe"):          # .exe is what Windows looks for
            f = self.pip_dir / name
            f.write_text("#!/bin/sh\n", encoding="utf-8")
            f.chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def test_pip_folder_added_when_yt_dlp_is_missing(self):
        with mock.patch.dict(os.environ, {"PATH": str(self.empty)}), \
                mock.patch.object(fetch, "pip_tool_dirs", return_value=[str(self.pip_dir)]):
            self.assertEqual(fetch.use_pip_tools(), str(self.pip_dir))
            self.assertEqual(os.environ["PATH"].split(os.pathsep), [str(self.empty), str(self.pip_dir)])

    def test_nothing_changes_when_yt_dlp_is_on_path(self):
        with mock.patch.dict(os.environ, {"PATH": str(self.pip_dir)}):
            self.assertIsNone(fetch.use_pip_tools())
            self.assertEqual(os.environ["PATH"], str(self.pip_dir))

    def test_nothing_found(self):
        with mock.patch.dict(os.environ, {"PATH": str(self.empty)}), \
                mock.patch.object(fetch, "pip_tool_dirs", return_value=[str(self.empty)]):
            self.assertIsNone(fetch.use_pip_tools())

    def test_pip_tool_dirs_include_this_pythons_folder(self):
        import sysconfig
        self.assertIn(sysconfig.get_path("scripts"), fetch.pip_tool_dirs())


if __name__ == "__main__":
    unittest.main()
