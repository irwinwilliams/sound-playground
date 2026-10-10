#!/usr/bin/env python3
"""Build standalone files into dist/.

- dist/recorder.html : the parent voice recorder, with word lists, pictures and
  audio processing copied from src/game.html so the two never drift apart.
- dist/game.html     : the game wrapped in a full HTML document for local testing.
                       Outside claude.ai it runs in device-only mode (localStorage,
                       stand-in computer voice).
"""
from pathlib import Path

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
print("Built dist/recorder.html and dist/game.html")
