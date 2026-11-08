"""Score every frame mode against the human labels.

    uv run python tests/score.py            # print the table
    uv run python tests/score.py --write    # also write tests/RESULTS.md
    uv run python tests/score.py --max-same 0   # without the repeated-slide cap
    uv run python tests/score.py --round 2      # one round only (no "round" field = round 1)

The modes are re-run on the saved scans with the CURRENT code, so a change to
ytconv/frames.py is scored the moment it is made - no re-download.

precision  of the frames a mode keeps, the share a person called useful
coverage   of the evenly sampled seconds a person called useful, the share whose
           picture some kept frame shows (same picture = thumbnail distance
           below frames.same_distance - 6, smaller on dark videos)
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from ytconv import frames, repeats  # noqa: E402
from build_testset import matching_label_second, modes  # noqa: E402

LABELS = ROOT / "tests" / "labels" / "frames.csv"


def load_labels():
    with open(LABELS, newline="") as fh:
        return {(r["video"], int(r["second"])): r["label"] for r in csv.DictReader(fh)}


def score_video(key, labels, max_same=repeats.MAX_SAME):
    d = ROOT / "testdata" / key
    scan = json.loads((d / "scan.json").read_text())
    meta = json.loads((d / "testset.json").read_text())
    by_sec = {f["second"]: f for f in scan}
    # the same rule the picker uses: smaller on dark videos (frames.same_distance)
    same = frames.same_distance(median(f["mean_lum"] for f in scan))
    sample = [int(s) for s, why in meta["queue"].items() if why == "sample"]
    labelled = [s for s in sample if (key, s) in labels]

    def label_of(sec):
        if (key, sec) in labels:
            return labels[(key, sec)]
        match = matching_label_second(sec, by_sec, labelled, same)
        return labels.get((key, match)) if match is not None else None

    useful_sample = [s for s in labelled if labels[(key, s)] == "useful"]
    rows = {}
    for mode, kept in modes(scan, key, max_same).items():
        got = [label_of(s) for s in kept]
        useful, not_useful = got.count("useful"), got.count("not")
        covered = sum(
            1 for s in useful_sample
            if any(frames._distance(by_sec[s]["lum"], by_sec[k]["lum"]) < same for k in kept))
        rows[mode] = {
            "kept": len(kept),
            "useful": useful,
            "not": not_useful,
            "unlabelled": sum(1 for g in got if g in (None, "skip")),
            "precision": useful / (useful + not_useful) if useful + not_useful else None,
            "coverage": covered / len(useful_sample) if useful_sample else None,
        }
    return rows, len(labelled), len(useful_sample)


def pct(x):
    return "  -  " if x is None else f"{x:5.0%}"


def add(total, r, n_useful):
    """Add one video's row for a mode to a running total."""
    total["useful"] += r["useful"]
    total["not"] += r["not"]
    if r["coverage"] is not None:
        total["cov_n"] += round(r["coverage"] * n_useful)
        total["cov_d"] += n_useful


def summary(t):
    """'73% (91/125)', '76% (48/63)' for a running total."""
    prec = t["useful"] / (t["useful"] + t["not"]) if t["useful"] + t["not"] else None
    cov = t["cov_n"] / t["cov_d"] if t["cov_d"] else None
    return (f"{pct(prec)} ({t['useful']}/{t['useful'] + t['not']})",
            f"{pct(cov)} ({t['cov_n']}/{t['cov_d']})")


def new_total():
    return {"useful": 0, "not": 0, "cov_n": 0, "cov_d": 0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true", help="also write tests/RESULTS.md")
    p.add_argument("--max-same", type=int, default=repeats.MAX_SAME,
                   help="the tool's repeated-slide cap (0 = off); needs "
                        "tests/build_repeats_cache.py to have run")
    p.add_argument("--round", type=int, default=None,
                   help="score one round only (a video with no round field is round 1)")
    args = p.parse_args()

    labels = load_labels()
    spec = json.loads((ROOT / "tests" / "testset.json").read_text())
    lines = ["| video | style | mode | kept | useful | not | precision | coverage |",
             "|---|---|---|---|---|---|---|---|"]
    totals, by_round, long_rows = {}, {}, []
    for v in spec["videos"]:
        key = v["key"]
        rnd = v.get("round", 1)
        if v.get("purpose") == "at" or not (ROOT / "testdata" / key / "scan.json").exists():
            continue
        if args.round is not None and rnd != args.round:
            continue
        rows, n_lab, n_useful = score_video(key, labels, args.max_same)
        for mode, r in rows.items():
            lines.append(f"| {key} | {v['style']} | {mode} | {r['kept']} | {r['useful']} | {r['not']} | "
                         f"{pct(r['precision'])} | {pct(r['coverage'])} |")
            add(totals.setdefault(mode, new_total()), r, n_useful)
            add(by_round.setdefault((rnd, mode), new_total()), r, n_useful)
        if v.get("long_gameplay"):
            t = new_total()
            add(t, rows["auto"], n_useful)
            long_rows.append((key, v["style"], rows["auto"]["kept"], t))
    lines.append("")
    lines.append("| all videos | mode | precision | coverage |")
    lines.append("|---|---|---|---|")
    for mode, t in totals.items():
        prec, cov = summary(t)
        lines.append(f"| | {mode} | {prec} | {cov} |")
    rounds = sorted({rnd for rnd, _ in by_round})
    if len(rounds) > 1:
        lines.append("")
        lines.append("| round | mode | precision | coverage |")
        lines.append("|---|---|---|---|")
        for rnd in rounds:
            for mode in totals:
                if (rnd, mode) in by_round:
                    prec, cov = summary(by_round[(rnd, mode)])
                    lines.append(f"| {rnd} | {mode} | {prec} | {cov} |")
    for key, style, kept, t in long_rows:
        prec, cov = summary(t)
        lines.append("")
        lines.append(f"Long gameplay video on its own ({key}, {style}), auto: {kept} kept, "
                     f"precision {prec.strip()}, coverage {cov.strip()}.")
    text = "\n".join(lines)
    print(text)
    if args.write:
        res = ROOT / "tests" / "RESULTS.md"
        # keep the sections other scripts add (--at, speech-to-text)
        old = res.read_text() if res.exists() else ""
        others = [sec for sec in old.split("\n## ")[1:]
                  if not sec.startswith("Frame picking")]   # this script's own section is rewritten
        rest = "".join("\n## " + sec for sec in others)
        res.write_text(
            "# Measured results\n\n## Frame picking against human labels\n\n"
            "Made by `tests/score.py` from the labels in `tests/labels/frames.csv`: "
            f"{len(labels)} frames, each looked at by a person and marked useful in notes "
            "or not. Rule used: a whiteboard frame where the presenter's body or hand "
            "covers the writing counts as not useful, unless they are pointing at it.\n\n"
            "precision = of the frames a mode keeps, the share a person called useful. "
            "coverage = of the useful moments in an even sample, the share some kept "
            "frame shows.\n\n"
            "auto = what the tool does when no mode flag is given: it looks at the "
            "video and picks default, motion4.5 (\"board\") or gameplay itself "
            "(frames.detect_mode). default, motion4.5 and auto keep up to 35 frames, or "
            "one per 20 s on videos longer than about 12 minutes (frames.auto_max_frames); "
            "gameplay and every keep up to 35.\n\n"
            + (f"default, motion4.5 and auto include the tool's repeated-slide cap (at most "
               f"{args.max_same} frames of one slide or board, ytconv/repeats.py); "
               "`tests/score.py --max-same 0` scores them without it.\n\n"
               if args.max_same else "default, motion4.5 and auto are scored WITHOUT the "
               "repeated-slide cap (--max-same 0).\n\n")
            + text + "\n" + rest)
        print("\nwrote tests/RESULTS.md")


if __name__ == "__main__":
    main()
