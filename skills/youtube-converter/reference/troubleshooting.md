# Troubleshooting

Read this when a download fails or comes back below 1080p, when frames come
back wrong, or before changing how the tool works.

## Clients, quality and failed downloads

The tool tries several yt-dlp "player clients" in turn, because YouTube blocks
some of them with HTTP 403 and which ones work changes over time. It also
keeps going when a client succeeds below 1080p: that download is held as a
fallback, and the other clients are asked (without downloading) whether they
can beat it. Lines like `[fetch] mweb offers only 360p - skipping` are normal.
If none reaches 1080p, it uses the best and says `no client delivered 1080p` -
the video is usually just not available in 1080p. Tell the user the
resolution; do not retry. If every
client fails, show the user the error exactly as printed - it lists the likely
causes in order: yt-dlp out of date, yt-dlp missing its JavaScript challenge
solver, or a network (often school or work Wi-Fi) blocking YouTube's video
servers.

To check whether YouTube or yt-dlp has broken the tool in general - only with a
cloned repo (a `PROJECT` line in Step 1) - run this: captions and search, about 15 seconds; without `--quick` it also
tests a download and frames (about a minute, 9 MB):

```bash
cd "PROJECT" && uv run python tests/healthcheck.py --quick
```

## When frames come back wrong

Re-run with `--debug-scores` and read `scores.csv`. The usual causes, in order:

1. **Everything dropped as "moving footage".** The automatic mode choice
   should catch this; if the printed mode was `default` and still almost
   nothing came through, read on. A handheld or zooming camera, or
   a presenter in shot, never holds still, so nothing passes the motion gate.
   **Vertical Shorts are the extreme case** - a talking head composited beside
   the diagram means no second is ever still, and every frame drops. Measured
   motion on such a short was 2.2-5.2 against a gate of 1.0. Re-run with
   `--motion-max 4.5` (add `--threshold 0.3` if still too few come through).
   If the video is gameplay or action rather than slides, use `--gameplay`
   instead - there, the moving seconds are the ones worth keeping.

   Do not change the 1.0 default - it is right for lecture screencasts.
2. **Everything "near-black".** Should no longer happen on dark tablet videos -
   the cutoff is relative to the video's own brightness (half its median, at
   most 12). If it does, use `--every 10` and tell the user.
3. **Everything "below threshold".** Low-contrast material - pencil on paper,
   a dim whiteboard. Try `--threshold 0.3`.
4. **Faces getting through.** The presenter sat still. Expected at a low rate,
   about 1 in 30 on screen-recorded video.

## Known pitfalls - do not re-solve these

- **The plain download 403s.** The fix is the player-client fallback chain in
  `ytconv/fetch.py`, not one hardcoded client.
- **yt-dlp's `--test` is not a 403 test.** It pulls about 10KB and passes on
  clients that fail the real download.
- **YouTube refuses auto-translated captions** with HTTP 429 ("too many
  requests"), and one refused track in a request used to abort the whole
  download. The tool fetches one track at a time; translate yourself (Step 4).
- **YouTube captions repeat every phrase two or three times.** The transcript
  step removes this; do not "simplify" the deduplication away.
- **Scene detection finds cuts to the presenter's face, not information.**
- **Edge density on a tiny 64x36 downscale ranks faces above code** - text is
  averaged out of existence at that size. Edges are detected at full
  resolution instead, with motion as the gate.
- **Matching slide text to speech to choose the `--at` frame was tested and
  lost** (20/45 against 29/45 for a fixed 8 s delay): titles appear before the
  diagram. Do not bring it back without beating the fresh test set.
- **zsh does not word-split unquoted variables.** Pass yt-dlp arguments as a
  Python list to `subprocess`, never as one shell string.
- **macOS has no `timeout` command.**
