#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps
import sys
BASE = Path(__file__).resolve().parents[1]
ORIG_DIR = BASE / 'images' / 'canva' / 'originals'
OUT_DIR = BASE / 'images' / 'canva'
print('ORIG_DIR:', ORIG_DIR)
print('OUT_DIR:', OUT_DIR)
if not ORIG_DIR.exists():
    print('ORIG_DIR missing')
    sys.exit(2)
# find a couple of known files
candidates = ['Home Page cover image.png','phuket beach2.jpg','pickleball 1.jpg']
for name in candidates:
    p = ORIG_DIR / name
    print(name, 'exists?', p.exists())
# Try opening and writing a test file
p = ORIG_DIR / 'Home Page cover image.png'
if p.exists():
    try:
        im = Image.open(p)
        im = ImageOps.exif_transpose(im)
        im = im.convert('RGB')
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        test_out = OUT_DIR / 'debug-hero-home.jpg'
        im.thumbnail((1600,900), Image.LANCZOS)
        im.save(test_out, format='JPEG', quality=75)
        print('WROTE', test_out)
    except Exception as e:
        print('ERROR processing', p, e)
else:
    print('sample source not found; listing directory:')
    for f in sorted(ORIG_DIR.iterdir()):
        print(' -', f.name)
