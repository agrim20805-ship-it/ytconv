"""--playlist: convert each video of a YouTube playlist into its own folder.

OUT/NN-<id>/ holds exactly what a single run writes. OUT/index.html and
OUT/index.md list every video with its status, and are rewritten after each
one, so a run that stops halfway still leaves a correct index. A folder that is
already complete is skipped, so running the same command again carries on.
"""

import copy
import json
import re
import sys
from pathlib import Path

from . import fetch, notes, research

DEFAULT_LIMIT = 10          # a 48-video playlist should not run for hours by accident
VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}")

WAITING, DONE, SKIPPED, NO_TRANSCRIPT = "waiting", "done", "skipped - already done", "no transcript"


class _LastLine:
    """Passes writes through to a stream and remembers the last non-empty line,
    so a failed video can be listed with the reason it gave."""

    def __init__(self, stream):
        self.stream, self.last, self._buf = stream, "", ""

    def write(self, text):
        self.stream.write(text)
        self._buf += text
        *done, self._buf = self._buf.split("\n")
        for line in done:
            if line.strip():
                self.last = line.strip()
        return len(text)

    def flush(self):
        self.stream.flush()

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def reason(self):
        return (self._buf.strip() or self.last)[:200]


def read_playlist(url):
    """(playlist title, playlist id, [{id, title, duration}]) in playlist order."""
    info = research._yt_json(["--flat-playlist", "-J", url])
    if info.get("_type") != "playlist" or info.get("entries") is None:
        raise ValueError("This link is a single video, not a playlist - leave out --playlist.")
    videos = []
    for e in info["entries"]:
        vid = (e or {}).get("id") or ""
        if VIDEO_ID.fullmatch(vid):
            videos.append({"id": vid, "title": e.get("title") or vid,
                           "duration": e.get("duration")})
    return info.get("title") or "Playlist", info.get("id") or "playlist", videos


def _complete(folder, args):
    """True when folder already holds what this command would write."""
    if not (folder / "transcript.txt").is_file():
        return False
    if not args.no_frames and not (folder / "frame-scores.json").is_file():
        return False
    if args.notes and not (folder / "notes.html").is_file():
        return False
    return True


def _watch_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"


def write_index(out, title, rows):
    """index.md and index.html: one row per video, with links to its files."""
    md = [f"# {title}", "", "| # | Video | Length | Status | Files |", "|---|---|---|---|---|"]
    html_rows = []
    for r in rows:
        length = notes._clock(r["duration"]) if r["duration"] else ""
        files = [(name, f"{r['folder']}/{name}") for name in ("transcript.txt", "notes.html")
                 if (out / r["folder"] / name).is_file()]
        safe_title = r["title"].replace("|", "/").replace("[", "(").replace("]", ")")
        md.append(f"| {r['position']} | [{safe_title}]({_watch_url(r['id'])}) | {length} | "
                  f"{r['status']} | " + ", ".join(f"[{n}]({h})" for n, h in files) + " |")
        links = ", ".join(f'<a href="{notes._e(h)}">{notes._e(n)}</a>'
                          for n, h in files if research._safe_href(h))
        html_rows.append(
            f"<tr><td>{r['position']}</td>"
            f'<td><a href="{notes._e(_watch_url(r["id"]))}" target="_blank" rel="noopener">'
            f"{notes._e(r['title'])}</a></td><td>{length}</td>"
            f"<td>{notes._e(r['status'])}</td><td>{links}</td></tr>")
    (out / "index.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    page = ['<!doctype html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<title>{notes._e(title)} - playlist</title>',
            f'<style>{notes.CSS}{research.EXTRA_CSS}</style>', '</head>', '<body>', '<main>',
            f"<h1>{notes._e(title)}</h1>",
            '<div class="tablewrap"><table><thead><tr><th>#</th><th>Video</th><th>Length</th>'
            '<th>Status</th><th>Files</th></tr></thead><tbody>',
            *html_rows, '</tbody></table></div>', '</main>', '</body>', '</html>']
    (out / "index.html").write_text("\n".join(page) + "\n", encoding="utf-8")
    (out / "index.json").write_text(json.dumps({"title": title, "videos": rows}, indent=1,
                                               ensure_ascii=False), encoding="utf-8")


def run(args, convert):
    """Convert the playlist in args.source with convert(args, is_local, local)."""
    try:
        title, list_id, videos = read_playlist(args.source)
    except (fetch.FetchError, ValueError) as exc:
        print(f"[playlist] {exc}", file=sys.stderr)
        return 1 if isinstance(exc, fetch.FetchError) else 2
    limit = DEFAULT_LIMIT if args.playlist_limit is None else args.playlist_limit
    todo = videos if limit == 0 else videos[:limit]
    out = Path(args.out) if args.out else Path("output") / (
        "playlist-" + (re.sub(r"[^A-Za-z0-9_-]", "", list_id) or "playlist"))
    out.mkdir(parents=True, exist_ok=True)
    print(f"[playlist] {title}: {len(videos)} videos; converting {len(todo)}"
          + ("" if len(todo) == len(videos) else
             f" (--playlist-limit {limit}; 0 converts all)") + f" into {out}", flush=True)

    width = max(2, len(str(len(videos))))
    rows = [{"position": n, "id": v["id"], "title": v["title"], "duration": v["duration"],
             "folder": f"{n:0{width}d}-{v['id']}", "status": WAITING}
            for n, v in enumerate(todo, 1)]
    write_index(out, title, rows)

    failed = 0
    for row in rows:
        folder = out / row["folder"]
        print(f"\n[playlist] {row['position']}/{len(rows)}: {row['title']}", flush=True)
        if _complete(folder, args):
            row["status"] = SKIPPED
            print(f"[playlist] {folder.name} is already done - skipping", flush=True)
            write_index(out, title, rows)
            continue
        one = copy.copy(args)
        one.source, one.out, one.playlist = _watch_url(row["id"]), str(folder), False
        err = _LastLine(sys.stderr)
        sys.stderr = err
        try:
            code = convert(one, False, Path(one.source))
        except KeyboardInterrupt:
            raise
        except Exception as exc:          # one broken video must not stop the rest
            code, err.last = 1, f"{type(exc).__name__}: {exc}"
        finally:
            sys.stderr = err.stream
        if code == 0:
            row["status"] = DONE if (folder / "transcript.txt").is_file() else NO_TRANSCRIPT
        else:
            failed += 1
            row["status"] = "failed: " + (err.reason() or f"exit code {code}")
        write_index(out, title, rows)

    done = sum(r["status"] in (DONE, SKIPPED) for r in rows)
    print(f"\n[playlist] {done} of {len(rows)} done, {failed} failed. "
          f"Index: {out / 'index.html'}", flush=True)
    return 0 if failed == 0 else 1
