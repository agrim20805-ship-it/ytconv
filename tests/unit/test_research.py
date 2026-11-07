"""Research mode's citation check, on a tiny fixture whose answers are known.

No network: the fixture is one fake converted video with a 3-line transcript.
"""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from ytconv import research

TRANSCRIPT = """[00:00] welcome to the lesson
[01:00] a black hole forms when a massive star collapses under gravity
[02:00] the event horizon is the point of no return
"""

NOTE = """# Fixture

## Black holes

- A massive star collapses under gravity into a black hole ([Fixture 01:00](https://www.youtube.com/watch?v=AAAAAAAAAAA&t=60s)).
- The event horizon is the point of no return ([Fixture 02:05](https://www.youtube.com/watch?v=AAAAAAAAAAA&t=125s)).
- Quasars outshine whole galaxies with radiation ([Fixture 00:00](https://www.youtube.com/watch?v=AAAAAAAAAAA&t=0s)).
- Neutron stars spin hundreds of times per second ([Fixture 09:00](https://www.youtube.com/watch?v=AAAAAAAAAAA&t=540s)).
- Another video entirely ([Other 00:10](https://www.youtube.com/watch?v=BBBBBBBBBBB&t=10s)).
- A massive star collapses into a black hole ([Fixture 02:40](https://www.youtube.com/watch?v=AAAAAAAAAAA&t=160s)).
"""


class CitationCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        folder = Path(cls.tmp.name)
        video = folder / "videos" / "AAAAAAAAAAA"
        video.mkdir(parents=True)
        (video / "transcript.txt").write_text(TRANSCRIPT, encoding="utf-8")
        (video / "metadata.json").write_text(
            json.dumps({"id": "AAAAAAAAAAA", "title": "Fixture", "duration": 180}),
            encoding="utf-8")
        (folder / "research.md").write_text(NOTE, encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            cls.result = research.build_page(folder)
        cls.printed = out.getvalue()
        cls.folder = folder

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_counts(self):
        self.assertEqual(self.result["citations"], 6)
        self.assertEqual(len(self.result["ok"]), 2)
        self.assertEqual(len(self.result["problems"]), 4)

    def test_summary_line(self):
        self.assertIn("6 timestamp citations across 1 converted videos: 2 ok, 4 to look at",
                      self.printed)

    def test_which_citations_pass(self):
        self.assertEqual(sorted(c["second"] for c in self.result["ok"]), [60, 125])

    def test_each_problem_has_the_right_reason(self):
        problems = {(c["video"], c["second"]): c["problem"] for c in self.result["problems"]}
        self.assertIn("shares 0", problems[("AAAAAAAAAAA", 0)])
        self.assertIn("past the end", problems[("AAAAAAAAAAA", 540)])
        self.assertIn("video not converted", problems[("BBBBBBBBBBB", 10)])
        self.assertIn("shares 0", problems[("AAAAAAAAAAA", 160)])

    def test_files_written(self):
        self.assertTrue((self.folder / "research.html").is_file())
        saved = json.loads((self.folder / "research-check.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["citations"], 6)


class CitedSeconds(unittest.TestCase):
    def test_forms(self):
        self.assertEqual(research._cited_seconds("&t=1m5s"), 65)
        self.assertEqual(research._cited_seconds("&t=65"), 65)
        self.assertEqual(research._cited_seconds("?t=2h"), 7200)
        self.assertEqual(research._cited_seconds("&t=1h2m3s"), 3723)
        self.assertEqual(research._cited_seconds("&t=0s"), 0)

    def test_a_link_without_a_time_is_not_a_citation(self):
        self.assertIsNone(research._cited_seconds("&list=PL1"))


class SafeHref(unittest.TestCase):
    def test_https_and_relative_paths_are_links(self):
        self.assertTrue(research._safe_href("https://www.youtube.com/watch?v=abc&t=65s"))
        self.assertTrue(research._safe_href("videos/a/frames/f.jpg"))

    def test_dangerous_links_are_refused(self):
        for url in ("javascript:alert(1)", "data:text/html,x", "//evil.example",
                    "file:///etc/passwd"):
            with self.subTest(url=url):
                self.assertFalse(research._safe_href(url))


if __name__ == "__main__":
    unittest.main()
