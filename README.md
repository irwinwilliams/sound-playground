# Sound Playground

Phonics games for 5–7 year olds, based on the sound-first approach of the *Mentava Alphabet Sounds* book: lowercase letters, letter **sounds** (not names), and blending without pausing. The book's text and illustrations are not included; all pictures here are original.

## Games

- **Slide & Blend**: the child slides a finger left to right along a word's letters without lifting. Each sound plays as the finger reaches it and blends into the next (held sounds loop while the finger rests on them). Then they pick the matching picture. Three levels: *Smooth starts* (man, sun), *Pop starts* (cat, bug), *Sound teams* (fish, frog).
- **Sound Twins**: the child hears one word and picks between two pictures that differ by one sound (fan / pan, mouse / mouth). Pairs the child misses come up more often.

## Parent features

- **Your voice**: every sound and word is recorded by the parent. 24 sounds + 55 words = 79 clips.
- **Progress report** (behind a press-and-hold gate): days and minutes played, first-try accuracy, a 14-day chart, a sound mastery grid, results by level and by sound pair, words to practise, and suggestions for what to practise next.
- **Children**: separate profiles and progress per child.

## Files

| Path | What it is |
|---|---|
| `src/game.html` | The game. Published as a claude.ai Artifact (page body only; the platform adds the document skeleton). |
| `src/recorder.template.html` | The parent voice recorder. Content and audio code are injected from `src/game.html` at build time. |
| `scripts/build.py` | Builds `dist/index.html`, `dist/recorder.html` and `dist/game.html`. |
| `.github/workflows/pages.yml` | Builds and deploys `dist/` to GitHub Pages. |

```sh
python3 scripts/build.py
```

## How the pieces fit

1. The parent opens `dist/recorder.html` directly in Chrome or Safari (the claude.ai frame blocks the microphone), records clips, and clicks **Save voice pack**. Clips are kept in IndexedDB until then.
2. In the game: hold **Grown-ups**, open **Voice studio**, click **Import voice pack**. Clips are trimmed, normalised, stored as 22.05 kHz 16-bit mono WAV (base64) and shared with everyone who plays that artifact.
3. Recordings can also be uploaded as individual files, or as one long take split automatically at the pauses.

## Data (Artifact `db` capability)

| Path | Contents | Access |
|---|---|---|
| `voice/<clip>` | `{wav, dur, sr, name, at}` | everyone reads; owner/editors write |
| `voicemeta/index` | `{<clip>: updatedAt}` | everyone reads; owner/editors write |
| `data/users/<uid>/profile` | `{kids[], activeKid, robot}` | private to each viewer |
| `data/users/<uid>/profile/k_<kidId>/<yyyy-mm-dd>` | `{d, a: [attempt…]}` one doc per child per day | private to each viewer |

Attempt fields: `g` game (`b` blend, `t` twins), `w` word, `f` foil word, `c` contrast id, `lv` level, `ok` first-try correct (0/1), `tr` tries, `sl` slides, `sm` used Show me, `rp` replays, `ms` time taken, `ts` timestamp.

Outside claude.ai (e.g. `dist/game.html`), the game falls back to localStorage and a stand-in computer voice.

## GitHub Pages

`.github/workflows/pages.yml` runs the build and publishes `dist/` on every push to `main`:

- `/` landing page
- `/recorder.html` the voice recorder (the microphone works here because Pages serves over https)
- `/game.html` a test copy of the games (computer voice, progress kept in that browser only)

Turn it on once: **Settings → Pages → Source: GitHub Actions**, or run
`gh api -X POST repos/<owner>/sound-playground/pages -f build_type=workflow`.

## Publishing to claude.ai

Publish `src/game.html` as an Artifact with capabilities:

```json
{"db": {"rules": [
  {"path": "voice", "read": "view", "write": "admin"},
  {"path": "voicemeta", "read": "view", "write": "admin"}
]}, "user": {}}
```
