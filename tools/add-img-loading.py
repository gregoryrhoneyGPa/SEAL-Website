#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = list(root.rglob('*.html')) + list(root.rglob('*.htm'))
changed = 0
for f in files:
    s = f.read_text(encoding='utf8', errors='replace')
    orig = s
    s = re.sub(r'<img((?![^>]*\bloading=)[^>]*?)>', r'<img\1 loading="lazy">', s, flags=re.IGNORECASE)
    if s != orig:
        f.write_text(s, encoding='utf8')
        changed += 1

print(f"Processed {len(files)} files, updated {changed} files.")
