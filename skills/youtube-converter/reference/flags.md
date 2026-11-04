# Flags and output files

Read this when you need a flag not shown in SKILL.md, or the list of files a
run writes. "Step N" means that step in SKILL.md.

## Flags worth knowing

- `--search "topic"` - research mode: list YouTube results with their details
  (research mode). `--results N` for more than 10 (at most 25).
- `--research-page DIR` - research mode: `research.md` -> `research.html`,
  with the citations checked (research mode).
- `--no-frames` - transcript only, no video download.
- `--lang CODE` - the spoken language when YouTube's label is wrong.
- `--translate [LANG]` - also write `transcript.LANG.txt` (default English).
- `--stt` - speech-to-text even if captions exist (or a subtitle file is there).
- `--no-stt` - a local video file: no speech-to-text, frames only.
- `--notes` - also write `notes.html` and `notes.md` (Step 5b).
- `--stt-engine faster-whisper|whisper.cpp` - pick the engine.
- `--at MM:SS` - the frame for a transcript moment (Step 6). Repeatable.
- `--mark`, `--clean-board` - boxed / presenter-free copies (Step 7).
  `--clean-board` is automatic in board mode; `--no-clean-board` skips it.
- `--max-same N` - at most N frames of one slide or board (default 2; 0 keeps
  every repeat). On by default; `repeats.json` lists what was dropped. Needs
  OCR (built in on a Mac); without it the tool says so and keeps everything.
- `--debug-scores` - writes `scores.csv` with the keep/drop reason for every
  second. Reach for this when frames come back wrong.
- `--threshold 0.3` - loosen selection when too few frames come through.
  Default is 0.5.
- `--max-frames 50` - cap on frames kept. Default is 35, or one per 20 s on
  videos longer than about 12 minutes.
- `--keep-video`, `--work-dir DIR` - keep the downloaded video
  (as `DIR/video.mp4`) instead of deleting it.
- `--gameplay` - fast footage: sharpest frames instead of still ones. Normally
  chosen automatically.
- `--every N` - one frame every N seconds, no filtering. Cannot be combined
  with `--gameplay`.
- `--motion-max N` - the stillness limit (1.0 for slides, 4.5 for a board;
  normally chosen automatically). Giving it turns off the automatic choice.
- `--client NAME` - force one yt-dlp player client instead of the fallback
  chain.

## What you get

| File | What it is |
|---|---|
| `transcript.txt` | `[MM:SS] text`, one line per caption, duplicates removed; header gives language and source |
| `transcript.LANG.txt` | with `--translate` |
| `metadata.json` | title, uploader, duration, chapters |
| `frames/frame_MM-SS.jpg` | slides, graphs, tables, code - native resolution |
| `frame-scores.json` | a score for every second - search this, never re-scan |
| `at.json` | with `--at`: the frame, the text read off it, whether it matched |
| `marked/`, `marked.json` | with `--mark` |
| `clean/`, `clean/clean.json` | board mode or `--clean-board`; `clean.json` says which copies are clean |
| `repeats.json` | slides or boards that were in more than 2 frames, and which 2 were kept |
| `notes.html`, `notes.md` | with `--notes` (Step 5b) |
| `search.json` | research mode: the search results and their details |
| `research.md`, `research.html` | research mode: the note you wrote, and its page |
| `research-check.json` | research mode: every citation checked, and paragraphs without one |
