#!/usr/bin/env python3
"""Web-optimize Canva originals: produce JPG + WebP outputs.
Usage: python webopt_canva.py
"""
try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False
from pathlib import Path
import sys
import shutil

BASE = Path(__file__).resolve().parents[1]
ORIG_DIR = BASE / 'images' / 'canva' / 'originals'
OUT_DIR = BASE / 'images' / 'canva'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# mapping: source filename (case-insensitive substring) -> output base name, target size (w,h)
MAPPINGS = [
    ("Home Page cover image", "hero-home", (1600,900)),
    ("phuket beach2", "hero-pickleball", (1600,900)),
    ("pickleball 1", "pickleball-1", (1200,800)),
    ("pickleball 2", "pickleball-2", (1200,800)),
    ("pickleball 4", "pickleball-3", (1200,800)),
]

# helper to find a matching file
def find_source(substring):
    s = substring.lower()
    for p in ORIG_DIR.iterdir():
        if p.is_file() and s in p.name.lower():
            return p
    return None


def process(src_path: Path, out_base: Path, size):
    jpg_path = out_base.with_suffix('.jpg')
    webp_path = out_base.with_suffix('.webp')
    if PIL_AVAILABLE:
        try:
            im = Image.open(src_path)
        except Exception as e:
            print(f"ERROR opening {src_path}: {e}")
            return False
        try:
            im = ImageOps.exif_transpose(im)
        except Exception:
            pass
        if im.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", im.size, (255,255,255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail(size, Image.LANCZOS)
        try:
            im.save(jpg_path, format='JPEG', quality=75, optimize=True)
            print(f"Wrote {jpg_path}")
        except Exception as e:
            print(f"ERROR saving JPG {jpg_path}: {e}")
        try:
            im.save(webp_path, format='WEBP', quality=75, method=6)
            print(f"Wrote {webp_path}")
        except Exception as e:
            print(f"ERROR saving WEBP {webp_path}: {e}")
        return True
    else:
        # Fallback: copy source file to jpg path (no conversion) and duplicate as webp if possible
        try:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            # copy original to jpg_path if original is already jpg-like
            shutil.copyfile(src_path, jpg_path)
            print(f"Copied {src_path.name} -> {jpg_path.name} (fallback)")
            # also create a copy for webp using same bytes (not a true webp)
            shutil.copyfile(src_path, webp_path)
            print(f"Copied {src_path.name} -> {webp_path.name} (fallback)")
            return True
        except Exception as e:
            print(f"FALLBACK ERROR copying {src_path}: {e}")
            return False


def main():
    if not ORIG_DIR.exists():
        print(f"Originals directory not found: {ORIG_DIR}")
        sys.exit(2)
    for src_sub, out_name, size in MAPPINGS:
        src = find_source(src_sub)
        if not src:
            print(f"Source for '{src_sub}' not found in {ORIG_DIR}")
            continue
        out_base = OUT_DIR / out_name
        process(src, out_base, size)

if __name__ == '__main__':
    main()
