# Listen (experimental)

Needs the cloned repo: the scripts live in `PROJECT/experiments/ears`, which is
not part of the pip package.

Only when the user asks what can be *heard* - sound effects, drops, a jump
scare. Tell them it is experimental: reliable for sound effects over speech or
quiet audio, structure only for music-heavy edits.

Work in `OUTDIR`, calling the scripts in `PROJECT/experiments/ears` by full
path. Follow the Commands section of `PROJECT/experiments/ears/README.md`:

1. Download the audio only, with the `web_embedded` client.
2. Set `DUR` to the seconds to analyse - the whole short, or one section of a
   long video. Every 2 seconds is one ffmpeg run.
3. Build `sheet.png` and look at it: tile 1 is 0-2s, tile 2 is 2-4s, left to
   right, top to bottom. Time runs left to right inside a tile, pitch bottom
   to top, brightness is loudness. A boom is a fading block at the bottom, a
   whoosh a grainy cloud up high, a riser a climbing line, a pop a small
   bright dot.
4. Run `detect.py` for candidate moments, and check each one on the sheet -
   it over-proposes on purpose.

Report what you hear with timestamps, and say how sure you are.
