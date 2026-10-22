#!/usr/bin/env python3
"""Build standalone files into dist/.

- dist/recorder.html : the parent voice recorder, with word lists, pictures and
  audio processing copied from src/game.html so the two never drift apart.
- dist/index.html    : a landing page linking the two (used for GitHub Pages).
- dist/game.html     : the game wrapped in a full HTML document for local testing.
                       Outside claude.ai it runs in device-only mode (localStorage,
                       stand-in computer voice).
"""
from pathlib import Path

INDEX = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sound Playground</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
<style>
:root{--bg:#edf3f7;--surface:#fff;--ink:#1c2433;--muted:#5a6578;--line:#d3dde7;--slide:#ffb529;--twin:#5a5fdc}
@media (prefers-color-scheme: dark){:root{--bg:#111723;--surface:#1a2231;--ink:#edf1f7;--muted:#9ba7ba;--line:#2d3749;color-scheme:dark}}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 "Atkinson Hyperlegible",system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:40px 16px}
h1{font:700 clamp(34px,7vw,48px)/1.1 Fredoka,system-ui,sans-serif;margin:0 0 8px}
h1 span{color:#e58a00}
p{color:var(--muted);max-width:60ch}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px;margin-top:28px}
a.card{display:block;text-decoration:none;color:inherit;background:var(--surface);border-radius:22px;padding:22px;box-shadow:inset 0 0 0 2px var(--line)}
a.card:hover,a.card:focus-visible{box-shadow:inset 0 0 0 3px var(--ink);outline:none}
a.card h2{font:600 24px/1.2 Fredoka,system-ui,sans-serif;margin:0 0 6px}
a.card.rec h2{color:#c42f43}
a.card p{margin:0;font-size:15px}
small{display:block;margin-top:32px;color:var(--muted)}
</style></head>
<body><main>
<h1>Sound <span>Playground</span></h1>
<p>Phonics games for 5–7 year olds: Slide &amp; Blend and Sound Twins. The games speak in a parent’s own voice, recorded with the recorder below.</p>
<div class="cards">
  <a class="card rec" href="recorder.html"><h2>Voice recorder</h2><p>Record each sound and word with your microphone, then save a voice pack to import into the game.</p></a>
  <a class="card" href="game.html"><h2>Try the games</h2><p>A test copy. It uses a computer voice and keeps progress only in this browser. The full version runs on claude.ai.</p></a>
</div>
<small>Sounds taught as sounds, not letter names. Lowercase first. Blend without pausing.</small>
</main></body></html>
"""

root = Path(__file__).resolve().parent.parent
game = (root / "src" / "game.html").read_text(encoding="utf-8")
tpl = (root / "src" / "recorder.template.html").read_text(encoding="utf-8")

def between(text, start, end):
    a = text.index(start)
    return text[a:text.index(end, a)]

content = between(game, "const SOUNDS = {", "/* ============================================================\n   STATE + STORAGE")
encode = between(game, "async function decodeMono", "/* Split one long")

dist = root / "dist"
dist.mkdir(exist_ok=True)
(dist / "recorder.html").write_text(
    tpl.replace("/*__CONTENT__*/", content).replace("/*__ENCODE__*/", encode), encoding="utf-8")
(dist / "game.html").write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<style>body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
    '</head><body>' + game + '</body></html>', encoding="utf-8")
(dist / "index.html").write_text(INDEX, encoding="utf-8")
print("Built dist/index.html, dist/recorder.html and dist/game.html")
