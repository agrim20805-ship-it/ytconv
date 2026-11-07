"""Small helpers: frame file names, clock times, and the MCP server's argument checks."""
import unittest

from ytconv import frames, mcp_server, notes


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


if __name__ == "__main__":
    unittest.main()
