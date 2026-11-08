# ytconv

Turns a YouTube video into study material: a clean transcript and only the
frames worth seeing - slides, diagrams, code - not the presenter's face.

<a href="https://www.youtube.com/shorts/72ZZiSuqWXU"><img src="https://img.youtube.com/vi/72ZZiSuqWXU/maxresdefault.jpg" alt="Watch the 30-second demo on YouTube" width="480"></a>

## What it does

- Transcripts from captions, or free speech-to-text on your computer
- Frames picked to suit slides, whiteboards or gameplay
- Translation, a notes page and local video files
- Research mode: compares videos on a topic, linking each claim to its moment

## Requirements

Python 3.9+, yt-dlp and ffmpeg. Run on macOS only
([platforms](https://github.com/agrim20805-ship-it/Youtuber-Converter/blob/main/GUIDE.md#requirements)). On a Mac:

```bash
brew install yt-dlp ffmpeg
pip install ytconv
```

Mac's built-in Python: use `pip3` and `python3 -m ytconv`. Python 3.11+:
`pip install "ytconv[full]"` also brings yt-dlp.

## Use

```bash
ytconv "URL"               # transcript + frames
ytconv "URL" --no-frames   # transcript only
ytconv "URL" --notes       # plus a notes page
ytconv "URL" --playlist    # every video in a playlist
ytconv --search "topic"    # research mode
```

`URL`: a YouTube link or video file. [Sample output](https://github.com/agrim20805-ship-it/Youtuber-Converter/tree/main/samples).

**With Claude:** includes a Claude Code skill and an MCP server
([setup](https://github.com/agrim20805-ship-it/Youtuber-Converter/blob/main/GUIDE.md#use-it-with-claude-code)).

**Tested** on 15 videos of eight kinds: 73% of kept frames useful on the first
six; kept frames show 61% of useful moments across all 15
([results](https://github.com/agrim20805-ship-it/Youtuber-Converter/blob/main/tests/RESULTS.md),
[every command checked](https://github.com/agrim20805-ship-it/Youtuber-Converter/blob/main/TESTED.md)).

**Disclaimer:** not affiliated with YouTube or Google. Use it only on videos
you have the right to download, for your own study. Provided as-is, with no
warranty. Built with AI assistance.

---

[Full guide](https://github.com/agrim20805-ship-it/Youtuber-Converter/blob/main/GUIDE.md).
