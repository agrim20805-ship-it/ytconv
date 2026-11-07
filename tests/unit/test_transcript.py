"""Caption parsing: rolling-caption duplicates removed, timestamps formatted.

No network, no yt-dlp or ffmpeg. Run from the repo root:
    python -m unittest discover -s tests/unit -v
"""
import tempfile
import unittest
from pathlib import Path

from ytconv import transcript

# YouTube's rolling captions: each cue repeats the line before it.
ROLLING_VTT = """WEBVTT

00:00:01.000 --> 00:00:03.000
supply and demand

00:00:03.000 --> 00:00:05.000
supply and demand
set the price

00:00:05.000 --> 00:00:07.000
set the price
of every good
"""


class ParseVtt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "rolling.vtt"
        with open(self.path, "w", encoding="utf-8", newline="\n") as f:   # Python 3.9 has no write_text(newline=)
            f.write(ROLLING_VTT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_rolling_captions_become_three_lines(self):
        lines, _ = transcript.parse_vtt(self.path)
        self.assertEqual(lines, ["[00:01] supply and demand",
                                 "[00:03] set the price",
                                 "[00:05] of every good"])

    def test_stats_count_the_duplicates_removed(self):
        _, stats = transcript.parse_vtt(self.path)
        self.assertEqual(stats["cues"], 3)
        self.assertEqual(stats["lines"], 3)
        self.assertEqual(stats["naive_chars"], 75)
        self.assertEqual(stats["chars"], 67)
        self.assertEqual(stats["last_timestamp"], 5)


class DropOverlap(unittest.TestCase):
    def test_overlapping_start_is_dropped(self):
        self.assertEqual(transcript._drop_overlap(["the", "cat", "sat"],
                                                  ["cat", "sat", "on", "the", "mat"]),
                         ["on", "the", "mat"])

    def test_no_overlap_keeps_everything(self):
        self.assertEqual(transcript._drop_overlap(["a", "b"], ["c", "d"]), ["c", "d"])

    def test_a_full_repeat_leaves_nothing(self):
        self.assertEqual(transcript._drop_overlap(["x", "the", "cat"], ["the", "cat"]), [])

    def test_first_cue_is_kept(self):
        self.assertEqual(transcript._drop_overlap([], ["hi"]), ["hi"])


class Stamp(unittest.TestCase):
    def test_short_form(self):
        self.assertEqual(transcript._stamp(65, False), "01:05")

    def test_long_form(self):
        self.assertEqual(transcript._stamp(3725, True), "1:02:05")


if __name__ == "__main__":
    unittest.main()
