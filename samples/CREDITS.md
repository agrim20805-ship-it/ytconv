# Samples and credits

What ytconv produced from three Creative Commons videos, so you can see the
output before installing anything.

- [`notes/`](notes/) - `ytconv URL --notes --max-frames 4` on the first video:
  the notes page (`notes.html`, `notes.md`), the transcript and 4 frames. The
  frame limit is lowered from the default to keep this folder small. The
  section summary was written by Claude from that section's transcript, as the
  skill does when asked.
- [`research/`](research/) - research mode on "What is copyright, and how do
  Creative Commons licences change it?", comparing all three videos. Claude
  wrote `research.md` from the transcripts; `ytconv --research-page` built
  `research.html` and checked the citations: 53 of 53 supported. The three
  videos were chosen for their licence, not taken from the search results.

All three videos are licensed **Creative Commons Attribution (CC BY)**, as
YouTube reports for each ("Creative Commons Attribution license (reuse
allowed)"), checked on 2026-11-08. The frames are stills from the video, and
the transcripts are the videos' own captions with timestamps added. Nothing else
was changed. Licence: https://creativecommons.org/licenses/by/3.0/

| Video | Channel | Link | Licence | Used in |
|---|---|---|---|---|
| Study Help: Understanding Copyright | University of South Australia | https://www.youtube.com/watch?v=psUEVRtYzpA | CC BY | notes, research |
| What is open knowledge? (A short history of copyright) | Wikimedia UK | https://www.youtube.com/watch?v=w4CcSfdC-PQ | CC BY | research |
| Creative Commons Explained (with captions) | Matt P. Wolf | https://www.youtube.com/watch?v=iBsoNSCmrno | CC BY | research |
