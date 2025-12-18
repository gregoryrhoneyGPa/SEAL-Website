from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
ORIG_DIR = BASE / 'images' / 'canva' / 'originals'
OUT_FILE = BASE / 'scripts' / 'webopt_log.txt'
MAPPINGS = [
    ("Home Page cover image", "hero-home"),
    ("phuket beach2", "hero-pickleball"),
    ("pickleball 1", "pickleball-1"),
    ("pickleball 2", "pickleball-2"),
    ("pickleball 4", "pickleball-3"),
]
lines = []
lines.append(f'ORIG_DIR: {ORIG_DIR}\n')
if not ORIG_DIR.exists():
    lines.append('ORIG_DIR missing\n')
else:
    files = list(sorted([p.name for p in ORIG_DIR.iterdir() if p.is_file()]))
    lines.append(f'Found {len(files)} files in originals:\n')
    for f in files:
        lines.append(' - ' + f + '\n')
    for sub, out in MAPPINGS:
        found = [f for f in files if sub.lower() in f.lower()]
        if found:
            lines.append(f"Mapping '{sub}' -> found: {found}\n")
        else:
            lines.append(f"Mapping '{sub}' -> NOT FOUND\n")
OUT_FILE.write_text(''.join(lines))
print('Wrote log to', OUT_FILE)
