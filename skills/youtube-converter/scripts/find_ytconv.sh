#!/usr/bin/env bash
# Prints the command that runs ytconv, for the youtube-converter skill.
#
#   line 1: the command to write wherever the skill says YTCONV
#   line 2: PROJECT=<path>, only when the skill sits inside a cloned repo
#
# Exit 0 when ytconv was found, 1 (with install help on stderr) when not.
# Never installs anything.

skill_dir=$(cd -P "$(dirname "$0")/.." 2>/dev/null && pwd -P)

# 1. The skill folder is <repo>/skills/youtube-converter (linked or not) and uv is here.
if [ -n "$skill_dir" ] && [ "$(basename "$(dirname "$skill_dir")")" = "skills" ]; then
    repo=$(cd -P "$skill_dir/../.." 2>/dev/null && pwd -P)
    if [ -f "$repo/pyproject.toml" ] && [ -d "$repo/ytconv" ]; then
        if command -v uv >/dev/null 2>&1; then
            printf 'cd "%s" && uv run python -m ytconv\n' "$repo"
            printf 'PROJECT=%s\n' "$repo"
            exit 0
        fi
        no_uv_repo=$repo
    fi
fi

# 2. Installed with pip, and its command is on PATH.
if command -v ytconv >/dev/null 2>&1; then
    echo "ytconv"
    exit 0
fi

# 3. Installed with pip, but the command folder is not on PATH.
#    Run from / so a folder called ytconv in the current folder cannot be picked up instead.
for py in python3 python; do
    if command -v "$py" >/dev/null 2>&1 && (cd / && "$py" -c "import ytconv" >/dev/null 2>&1); then
        echo "$py -m ytconv"
        exit 0
    fi
done

# 4. Nothing found. Say how to get it; install nothing.
{
    echo "ytconv is not installed."
    if [ -n "$no_uv_repo" ]; then
        echo "The cloned repo is at $no_uv_repo, but uv is missing."
        echo "Either install uv, or follow the pip setup in GUIDE.md (\"Without uv\")."
    fi
    echo "Install it with:  pip install ytconv"
    echo "It also needs yt-dlp and ffmpeg. On a Mac:  brew install yt-dlp ffmpeg"
    echo "Windows and Linux: see the Requirements section of GUIDE.md"
    echo "(https://github.com/agrim20805-ship-it/Youtuber-Converter/blob/main/GUIDE.md)."
} >&2
exit 1
