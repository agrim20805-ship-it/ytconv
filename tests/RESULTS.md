# Measured results

## Frame picking against human labels

Made by `tests/score.py` from the labels in `tests/labels/frames.csv`: 926 frames, each looked at by a person and marked useful in notes or not. Rule used: a whiteboard frame where the presenter's body or hand covers the writing counts as not useful, unless they are pointing at it.

precision = of the frames a mode keeps, the share a person called useful. coverage = of the useful moments in an even sample, the share some kept frame shows.

auto = what the tool does when no mode flag is given: it looks at the video and picks default, motion4.5 ("board") or gameplay itself (frames.detect_mode). default, motion4.5 and auto keep up to 35 frames, or one per 20 s on videos longer than about 12 minutes (frames.auto_max_frames); gameplay and every keep up to 35.

default, motion4.5 and auto include the tool's repeated-slide cap (at most 2 frames of one slide or board, ytconv/repeats.py); `tests/score.py --max-same 0` scores them without it.

| video | style | mode | kept | useful | not | precision | coverage |
|---|---|---|---|---|---|---|---|
| slides | light slides, presenter cut-ins | default | 36 | 31 | 4 |   89% |   65% |
| slides | light slides, presenter cut-ins | motion4.5 | 46 | 25 | 5 |   83% |   53% |
| slides | light slides, presenter cut-ins | gameplay | 35 | 2 | 8 |   20% |   29% |
| slides | light slides, presenter cut-ins | every | 35 | 4 | 4 |   50% |   35% |
| slides | light slides, presenter cut-ins | auto | 36 | 31 | 4 |   89% |   65% |
| screen | dark screen recording | default | 38 | 24 | 12 |   67% |   90% |
| screen | dark screen recording | motion4.5 | 43 | 18 | 11 |   62% |   85% |
| screen | dark screen recording | gameplay | 35 | 13 | 5 |   72% |    5% |
| screen | dark screen recording | every | 35 | 13 | 8 |   62% |   85% |
| screen | dark screen recording | auto | 38 | 24 | 12 |   67% |   90% |
| whiteboard | whiteboard, handwriting | default | 19 | 4 | 13 |   24% |   62% |
| whiteboard | whiteboard, handwriting | motion4.5 | 16 | 6 | 10 |   38% |   75% |
| whiteboard | whiteboard, handwriting | gameplay | 35 | 10 | 15 |   40% |   88% |
| whiteboard | whiteboard, handwriting | every | 34 | 8 | 16 |   33% |   62% |
| whiteboard | whiteboard, handwriting | auto | 16 | 6 | 10 |   38% |   75% |
| tablet | tablet drawing, no presenter | default | 5 | 4 | 1 |   80% |  100% |
| tablet | tablet drawing, no presenter | motion4.5 | 5 | 4 | 1 |   80% |  100% |
| tablet | tablet drawing, no presenter | gameplay | 30 | 9 | 21 |   30% |  100% |
| tablet | tablet drawing, no presenter | every | 35 | 12 | 21 |   36% |  100% |
| tablet | tablet drawing, no presenter | auto | 5 | 4 | 1 |   80% |  100% |
| hindi | Hindi speech, English slides and writing, presenter | default | 30 | 12 | 1 |   92% |   25% |
| hindi | Hindi speech, English slides and writing, presenter | motion4.5 | 28 | 24 | 4 |   86% |   25% |
| hindi | Hindi speech, English slides and writing, presenter | gameplay | 35 | 8 | 5 |   62% |   25% |
| hindi | Hindi speech, English slides and writing, presenter | every | 35 | 5 | 5 |   50% |   25% |
| hindi | Hindi speech, English slides and writing, presenter | auto | 28 | 24 | 4 |   86% |   25% |
| gameplay | gameplay Short, fast motion | default | 1 | 0 | 1 |    0% |   20% |
| gameplay | gameplay Short, fast motion | motion4.5 | 2 | 0 | 2 |    0% |   20% |
| gameplay | gameplay Short, fast motion | gameplay | 5 | 2 | 3 |   40% |   60% |
| gameplay | gameplay Short, fast motion | every | 2 | 1 | 1 |   50% |   20% |
| gameplay | gameplay Short, fast motion | auto | 5 | 2 | 3 |   40% |   60% |
| r2-slidespen | slides with pen notes, voice-over | default | 12 | 12 | 0 |  100% |  100% |
| r2-slidespen | slides with pen notes, voice-over | motion4.5 | 12 | 12 | 0 |  100% |  100% |
| r2-slidespen | slides with pen notes, voice-over | gameplay | 35 | 17 | 0 |  100% |  100% |
| r2-slidespen | slides with pen notes, voice-over | every | 35 | 9 | 0 |  100% |  100% |
| r2-slidespen | slides with pen notes, voice-over | auto | 12 | 12 | 0 |  100% |  100% |
| r2-french | French slides, voice-over | default | 16 | 16 | 0 |  100% |   57% |
| r2-french | French slides, voice-over | motion4.5 | 16 | 16 | 0 |  100% |   57% |
| r2-french | French slides, voice-over | gameplay | 31 | 23 | 0 |  100% |   51% |
| r2-french | French slides, voice-over | every | 35 | 7 | 0 |  100% |   86% |
| r2-french | French slides, voice-over | auto | 16 | 16 | 0 |  100% |   57% |
| r2-excel | Excel screen recording | default | 18 | 18 | 0 |  100% |   85% |
| r2-excel | Excel screen recording | motion4.5 | 19 | 18 | 1 |   95% |   85% |
| r2-excel | Excel screen recording | gameplay | 35 | 33 | 2 |   94% |   82% |
| r2-excel | Excel screen recording | every | 35 | 32 | 2 |   94% |   76% |
| r2-excel | Excel screen recording | auto | 18 | 18 | 0 |  100% |   85% |
| r2-whiteboard | physical whiteboard, presenter writing | default | 51 | 17 | 0 |  100% |   26% |
| r2-whiteboard | physical whiteboard, presenter writing | motion4.5 | 44 | 15 | 0 |  100% |   23% |
| r2-whiteboard | physical whiteboard, presenter writing | gameplay | 35 | 16 | 0 |  100% |    9% |
| r2-whiteboard | physical whiteboard, presenter writing | every | 35 | 7 | 0 |  100% |    6% |
| r2-whiteboard | physical whiteboard, presenter writing | auto | 35 | 16 | 0 |  100% |    9% |
| r2-german | German, presenter in front of slides | default | 28 | 21 | 0 |  100% |   91% |
| r2-german | German, presenter in front of slides | motion4.5 | 36 | 36 | 0 |  100% |   94% |
| r2-german | German, presenter in front of slides | gameplay | 35 | 21 | 0 |  100% |   57% |
| r2-german | German, presenter in front of slides | every | 35 | 7 | 0 |  100% |   91% |
| r2-german | German, presenter in front of slides | auto | 36 | 36 | 0 |  100% |   94% |
| r2-minecraft | long gameplay (Minecraft, 28 min) | default | 38 | 13 | 0 |  100% |   17% |
| r2-minecraft | long gameplay (Minecraft, 28 min) | motion4.5 | 56 | 14 | 1 |   93% |   17% |
| r2-minecraft | long gameplay (Minecraft, 28 min) | gameplay | 35 | 13 | 2 |   87% |    7% |
| r2-minecraft | long gameplay (Minecraft, 28 min) | every | 35 | 6 | 0 |  100% |    0% |
| r2-minecraft | long gameplay (Minecraft, 28 min) | auto | 35 | 13 | 2 |   87% |    7% |
| r2-lightboard | lightboard, presenter writing on glass | default | 20 | 11 | 0 |  100% |   43% |
| r2-lightboard | lightboard, presenter writing on glass | motion4.5 | 28 | 19 | 0 |  100% |   51% |
| r2-lightboard | lightboard, presenter writing on glass | gameplay | 35 | 20 | 0 |  100% |   43% |
| r2-lightboard | lightboard, presenter writing on glass | every | 35 | 6 | 0 |  100% |   60% |
| r2-lightboard | lightboard, presenter writing on glass | auto | 28 | 19 | 0 |  100% |   51% |
| r2-tablet | tablet handwriting on black | default | 17 | 14 | 0 |  100% |   74% |
| r2-tablet | tablet handwriting on black | motion4.5 | 17 | 14 | 0 |  100% |   74% |
| r2-tablet | tablet handwriting on black | gameplay | 30 | 27 | 0 |  100% |   74% |
| r2-tablet | tablet handwriting on black | every | 35 | 33 | 0 |  100% |   97% |
| r2-tablet | tablet handwriting on black | auto | 17 | 14 | 0 |  100% |   74% |
| r2-cartoon | cartoon animation | default | 31 | 31 | 0 |  100% |   37% |
| r2-cartoon | cartoon animation | motion4.5 | 31 | 31 | 0 |  100% |   37% |
| r2-cartoon | cartoon animation | gameplay | 35 | 28 | 0 |  100% |   31% |
| r2-cartoon | cartoon animation | every | 35 | 15 | 0 |  100% |   14% |
| r2-cartoon | cartoon animation | auto | 31 | 31 | 0 |  100% |   37% |

| all videos | mode | precision | coverage |
|---|---|---|---|
| | default |   88% (228/260) |   62% (228/370) |
| | motion4.5 |   88% (252/287) |   62% (229/370) |
| | gameplay |   80% (242/303) |   49% (183/370) |
| | every |   74% (165/222) |   60% (223/370) |
| | auto |   88% (266/302) |   61% (226/370) |

| round | mode | precision | coverage |
|---|---|---|---|
| 1 | default |   70% (75/107) |   71% (45/63) |
| 1 | motion4.5 |   70% (77/110) |   68% (43/63) |
| 1 | gameplay |   44% (44/101) |   41% (26/63) |
| 1 | every |   44% (43/98) |   62% (39/63) |
| 1 | auto |   73% (91/125) |   76% (48/63) |
| 2 | default |  100% (153/153) |   60% (183/307) |
| 2 | motion4.5 |   99% (175/177) |   61% (186/307) |
| 2 | gameplay |   98% (198/202) |   51% (157/307) |
| 2 | every |   98% (122/124) |   60% (184/307) |
| 2 | auto |   99% (175/177) |   58% (178/307) |

Long gameplay video on its own (r2-minecraft, long gameplay (Minecraft, 28 min)), auto: 35 kept, precision 87% (13/15), coverage 7% (2/29).

## Round 2 (2026-11-07)

Nine new videos from nine channels not used before (`"round": 2` in `tests/testset.json`),
chosen before any were scanned, and run with the code frozen at commit e96bace: automatic
mode, default settings. 522 new frames, each labelled by a person. Round 1 is unchanged.

| auto mode | precision | coverage |
|---|---|---|
| Round 1 (6 videos) | 73% (91/125) | 76% (48/63) |
| Round 2 (9 videos) | 99% (175/177) | 58% (178/307) |
| Combined | 88% (266/302) | 61% (226/370) |

Long gameplay video on its own (r2-minecraft, 28 min): 35 kept, precision 87% (13/15),
coverage 7% (2/29).

**Read round 2's precision with care.** Its labeller called 98% of all queued frames useful
(511 of 522), where round 1's called 48% useful (163 of 342). With labels that generous,
precision cannot separate good picking from bad: one frame every 10 seconds, with no
filtering at all, also scores 98% (122/124) on round 2. The combined precision is pulled up by
this, not by better picking.

**Coverage is the more telling round-2 number, and it is lower:** 58% against 76%. The
weakest videos were the physical whiteboard (9%), the long gameplay video (7%) and the cartoon
(37%): on all three the tool keeps frames from a few moments and misses most of the rest.

51 of the 228 frames auto mode keeps in round 2 have no label of their own and no labelled
neighbour showing the same picture, so they are left out of precision.

## --at against human answers

A hit is within 6 s of the second a person marked as the first clear appearance. "design" moments are the ones the rules were chosen from; "fresh" moments were picked from transcripts alone and labelled afterwards, so they are the honest measure. Made by `tests/score_at.py`.

| set | video | said at | person | said-at | said-at+8 (--at) | old --at | text match | how |
|---|---|---|---|---|---|---|---|---|
| design | slides | 02:59 | +0s | ✓ +0s | ✗ +8s | ✗ - | ✓ +1s | text: fullest, possibilitie, curve, produced |
| design | slides | 06:29 | not shown | ✗ +0s | ✗ +8s | ✗ +95s | ✗ +8s | +8 s |
| design | slides | 07:16 | +28s | ✗ +0s | ✗ +8s | ✗ +48s | ✓ +22s | text: good, production, possibilitie, curve |
| design | slides | 08:58 | +4s | ✓ +0s | ✓ +8s | ✗ +103s | ✗ +11s | text: ppc, topic, 1, 2 |
| design | slides | 14:36 | +12s | ✗ +0s | ✓ +8s | ✗ +4s | ✗ +0s | text: cars, produced, number, take |
| design | slides | 16:57 | +8s | ✗ +0s | ✓ +8s | ✗ +65s | ✓ +5s | text: sick, people, good, price |
| design | screen | 01:34 | +36s | ✗ +0s | ✗ +8s | ✗ +4s | ✗ +2s | text: keep, small, context |
| design | screen | 04:20 | not shown | ✗ +0s | ✗ +8s | ✗ +51s | ✗ +6s | text: execution, plan, check |
| design | screen | 08:06 | +8s | ✗ +0s | ✓ +8s | ✗ +62s | ✗ +0s | text: version, elegant, set, update |
| design | screen | 09:46 | not shown | ✗ +0s | ✗ +8s | ✗ +86s | ✗ +19s | text: inspiration, clone, site, 22 |
| design | screen | 11:34 | +60s | ✗ +0s | ✗ +8s | ✗ +17s | ✗ +0s | text: endpoint, database, direct, read |
| design | screen | 15:31 | +16s | ✗ +0s | ✗ +8s | ✗ +6s | ✗ +0s | text: live, before, documentation, current |
| design | whiteboard | 00:05 | +4s | ✓ +0s | ✓ +8s | ✗ +108s | ✗ +17s | text: 4, large, resistor, load |
| design | whiteboard | 00:30 | +8s | ✗ +0s | ✓ +8s | ✗ +83s | ✓ +8s | +8 s |
| design | whiteboard | 01:24 | +32s | ✗ +0s | ✗ +8s | ✗ +99s | ✗ +0s | text: 4, meter, resistor, load |
| design | whiteboard | 02:58 | +8s | ✗ +0s | ✓ +8s | ✗ +108s | ✓ +8s | text: 1, volt, 2 |
| design | whiteboard | 04:00 | +8s | ✗ +0s | ✓ +8s | ✗ +46s | ✗ +17s | text: 1, 5, volt, current |
| design | whiteboard | 05:02 | +8s | ✗ +0s | ✓ +8s | ✗ - | ✓ +8s | +8 s |
| design | tablet | 00:54 | +8s | ✗ +0s | ✓ +8s | ✗ +100s | ✓ +8s | +8 s |
| design | tablet | 01:48 | +8s | ✗ +0s | ✓ +8s | ✗ +95s | ✓ +8s | +8 s |
| design | tablet | 02:42 | +8s | ✗ +0s | ✓ +8s | ✗ +117s | ✓ +8s | +8 s |
| design | tablet | 03:12 | +8s | ✗ +0s | ✓ +8s | ✗ +111s | ✓ +8s | +8 s |
| design | tablet | 04:08 | +8s | ✗ +0s | ✓ +8s | ✗ +109s | ✓ +8s | +8 s |
| design | tablet | 05:20 | +8s | ✗ +0s | ✓ +8s | ✗ +88s | ✓ +8s | +8 s |
| design | hindi | 01:17 | +8s | ✗ +0s | ✓ +8s | ✗ - | ✓ +7s | text: irctc, database, dbms |
| design | hindi | 02:04 | +8s | ✗ +0s | ✓ +8s | ✗ - | ✓ +12s | text: data, database |
| design | hindi | 03:04 | +32s | ✗ +0s | ✗ +8s | ✗ +81s | ✗ +5s | text: base, data, related, database |
| design | hindi | 07:15 | +8s | ✗ +0s | ✓ +8s | ✓ +3s | ✗ +22s | text: table, data |
| design | hindi | 08:15 | +8s | ✗ +0s | ✓ +8s | ✗ +76s | ✗ +0s | text: irctc, system |
| design | hindi | 09:15 | +8s | ✗ +0s | ✓ +8s | ✗ +16s | ✓ +8s | +8 s |
| fresh | voiceslides | 00:52 | +8s | ✗ +0s | ✓ +8s | ✗ +38s | ✗ +1s | text: ways, list, two, memory |
| fresh | voiceslides | 01:45 | +4s | ✓ +0s | ✓ +8s | ✗ +44s | ✓ +0s | text: only, list, linked, single |
| fresh | voiceslides | 02:19 | +4s | ✓ +0s | ✓ +8s | ✓ +10s | ✗ +29s | text: made, part, consist, link |
| fresh | voiceslides | 02:46 | +12s | ✗ +0s | ✓ +8s | ✓ +7s | ✗ +0s | text: made, actual, part, contain |
| fresh | voiceslides | 05:14 | +4s | ✓ +0s | ✓ +8s | ✗ +59s | ✓ +0s | text: first, list, linked, access |
| fresh | code | 01:38 | +8s | ✗ +0s | ✓ +8s | ✗ +120s | ✓ +8s | +8 s |
| fresh | code | 05:14 | +8s | ✗ +0s | ✓ +8s | ✗ +90s | ✓ +8s | +8 s |
| fresh | code | 09:42 | +4s | ✓ +0s | ✓ +8s | ✗ +88s | ✓ +8s | +8 s |
| fresh | code | 12:00 | +0s | ✓ +0s | ✗ +8s | ✗ +7s | ✗ +8s | +8 s |
| fresh | code | 12:41 | +0s | ✓ +0s | ✗ +8s | ✗ +102s | ✗ +8s | +8 s |
| fresh | hinditree | 01:52 | +60s | ✗ +0s | ✗ +8s | ✗ - | ✗ +8s | +8 s |
| fresh | hinditree | 03:17 | +40s | ✗ +0s | ✗ +8s | ✗ +99s | ✗ +3s | text: tree |
| fresh | hinditree | 05:05 | +28s | ✗ +0s | ✗ +8s | ✗ +21s | ✗ +14s | text: avl, tree |
| fresh | hinditree | 06:34 | +32s | ✗ +0s | ✗ +8s | ✗ +58s | ✗ +18s | text: height |
| fresh | hinditree | 07:17 | +12s | ✗ +0s | ✓ +8s | ✓ +15s | ✗ +1s | text: 1, 2 |

| set | moments | said-at | said-at+8 (--at) | old --at | text match |
|---|---|---|---|---|---|
| design | 30 | 3/30 (10%) | 20/30 (67%) | 1/30 (3%) | 15/30 (50%) |
| fresh | 15 | 6/15 (40%) | 9/15 (60%) | 3/15 (20%) | 5/15 (33%) |

## Speech-to-text against human subtitles

First 5 minutes of each video, Whisper `small` model, on a Mac (M4 Pro). faster-whisper runs on the CPU; Homebrew's whisper.cpp can use the Mac's GPU, which is the likely reason it is faster. The reference is the uploader's own subtitles, which are lightly edited, so part of the error rate is wording, not mistakes. Made by `tests/score_stt.py`.

| check | video | engine | result | speed |
|---|---|---|---|---|
| transcribe | econ lecture (English) | faster-whisper | 5.3% word error rate | 70 s for 300 s of audio (4.3x real time) |
| transcribe | econ lecture (English) | whisper.cpp | 5.2% word error rate | 38 s for 300 s of audio (7.9x real time) |
| translate | Hindi DBMS lecture -> English | faster-whisper | 80% of the reference's content words came back | 32 s for 300 s of audio (9.5x real time) |
| translate | Hindi DBMS lecture -> English | whisper.cpp | 81% of the reference's content words came back | 7 s for 300 s of audio (40.4x real time) |

## Presenter removed (--clean-board) against human labels

The frames auto mode keeps on the board videos, each labelled twice: the original and its copy with the presenter removed (the median of the next 40 s). "The tool's choice" = what the notes page shows: the clean copy when its ghost share is at most 0.14 (frames.ghost_share), else the original. That cut-off was tuned on these same frames. Made by `tests/score_clean.py`.

| video | frames | original useful | presenter removed useful | better | worse | the tool's choice useful |
|---|---|---|---|---|---|---|
| whiteboard | 11 | 5 (45%) | 11 (100%) | 6 | 0 | 11 (100%) |
| hindi | 24 | 23 (96%) | 16 (67%) | 0 | 7 | 22 (92%) |
