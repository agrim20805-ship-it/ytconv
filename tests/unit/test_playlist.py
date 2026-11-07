"""--playlist without the network: a fake playlist and a fake converter."""
import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ytconv import playlist

VIDEOS = [{"id": "AAAAAAAAAAA", "title": "First", "duration": 99},
          {"id": "BBBBBBBBBBB", "title": "Second <script>alert(1)</script>", "duration": 732},
          {"id": "CCCCCCCCCCC", "title": "Third | with [brackets]", "duration": None},
          {"id": "DDDDDDDDDDD", "title": "Fourth", "duration": 60}]


def fake_convert(args, is_local, local):
    """Writes a transcript, except: B fails with a message, C crashes."""
    vid = args.source.rsplit("=", 1)[1]
    if vid == "BBBBBBBBBBB":
        print("Could not download the video.\nHTTP Error 403: Forbidden", file=__import__("sys").stderr)
        return 1
    if vid == "CCCCCCCCCCC":
        raise RuntimeError("something broke")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcript.txt").write_text("[00:00] hello\n", encoding="utf-8")
    return 0


class Playlist(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_playlist(self, limit=None, convert=fake_convert):
        args = argparse.Namespace(source="https://www.youtube.com/playlist?list=PLx", out=str(self.out),
                                  playlist=True, playlist_limit=limit, no_frames=True, notes=False)
        with mock.patch.object(playlist, "read_playlist", return_value=("Test list", "PLx", VIDEOS)), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = playlist.run(args, convert)
        return code, json.loads((self.out / "index.json").read_text(encoding="utf-8"))

    def test_failures_do_not_stop_the_rest(self):
        code, index = self.run_playlist()
        status = {r["id"]: r["status"] for r in index["videos"]}
        self.assertEqual(code, 1)
        self.assertEqual(status["AAAAAAAAAAA"], "done")
        self.assertEqual(status["BBBBBBBBBBB"], "failed: HTTP Error 403: Forbidden")
        self.assertEqual(status["CCCCCCCCCCC"], "failed: RuntimeError: something broke")
        self.assertEqual(status["DDDDDDDDDDD"], "done")

    def test_folders_are_numbered_in_playlist_order(self):
        _, index = self.run_playlist()
        self.assertEqual([r["folder"] for r in index["videos"]],
                         ["01-AAAAAAAAAAA", "02-BBBBBBBBBBB", "03-CCCCCCCCCCC", "04-DDDDDDDDDDD"])

    def test_limit(self):
        _, index = self.run_playlist(limit=2)
        self.assertEqual(len(index["videos"]), 2)
        _, index = self.run_playlist(limit=0)
        self.assertEqual(len(index["videos"]), 4)

    def test_rerun_skips_finished_videos(self):
        self.run_playlist()
        calls = []

        def counting(args, is_local, local):
            calls.append(args.source)
            return fake_convert(args, is_local, local)
        _, index = self.run_playlist(convert=counting)
        status = {r["id"]: r["status"] for r in index["videos"]}
        self.assertEqual(status["AAAAAAAAAAA"], "skipped - already done")
        self.assertEqual(status["DDDDDDDDDDD"], "skipped - already done")
        self.assertEqual(len(calls), 2)       # only the two that failed are tried again

    def test_index_pages_escape_titles(self):
        self.run_playlist()
        page = (self.out / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn('<a href="01-AAAAAAAAAAA/transcript.txt">transcript.txt</a>', page)
        md = (self.out / "index.md").read_text(encoding="utf-8")
        self.assertIn("Third / with (brackets)", md)     # cannot break the table or a link
        self.assertIn("| 1 | [First](https://www.youtube.com/watch?v=AAAAAAAAAAA) | 01:39 | done |", md)


if __name__ == "__main__":
    unittest.main()
