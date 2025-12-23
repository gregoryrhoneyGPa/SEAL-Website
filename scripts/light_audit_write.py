#!/usr/bin/env python3
import re
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
html_files = list(BASE.glob('**/*.htm*'))
img_tag_re = re.compile(r'<img\s+[^>]*>', re.I)
alt_re = re.compile(r'alt\s*=\s*["\'](.*?)["\']', re.I)
src_re = re.compile(r'src\s*=\s*["\'](.*?)["\']', re.I)
meta_desc_re = re.compile(r'<meta\s+name=["\']description["\']', re.I)
canonical_re = re.compile(r'rel=["\']canonical["\']', re.I)
h1_re = re.compile(r'<h1\b', re.I)

summary = []
missing_images_total = set()
files_report = []
for f in sorted(html_files):
    try:
        text = f.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        text = f.read_text(errors='ignore')
    imgs = img_tag_re.findall(text)
    img_count = len(imgs)
    missing_alts = []
    empty_alts = []
    missing_files = []
    for tag in imgs:
        alt_m = alt_re.search(tag)
        if not alt_m:
            missing_alts.append(tag)
        else:
            if alt_m.group(1).strip()=='' :
                empty_alts.append(tag)
        src_m = src_re.search(tag)
        if src_m:
            src = src_m.group(1)
            if not (src.startswith('http://') or src.startswith('https://') or src.startswith('//')):
                src_path = (f.parent / src).resolve()
                if not src_path.exists():
                    missing_files.append(src)
                    missing_images_total.add(str(src))
    has_meta_desc = bool(meta_desc_re.search(text))
    has_canonical = bool(canonical_re.search(text))
    h1_count = len(h1_re.findall(text))
    files_report.append({
        'file': str(f.relative_to(BASE)),
        'img_count': img_count,
        'missing_alt_count': len(missing_alts),
        'empty_alt_count': len(empty_alts),
        'missing_files': missing_files,
        'has_meta_description': has_meta_desc,
        'has_canonical': has_canonical,
        'h1_count': h1_count,
    })

out = []
out.append('Lightweight HTML Audit Report')
out.append(f'Base: {BASE}')
out.append(f'Files scanned: {len(files_report)}')
out.append('')
for r in files_report:
    out.append(f"- {r['file']}: imgs={r['img_count']}, missing_alt={r['missing_alt_count']}, empty_alt={r['empty_alt_count']}, h1={r['h1_count']}, meta_desc={r['has_meta_description']}, canonical={r['has_canonical']}")
    if r['missing_files']:
        for m in r['missing_files']:
            out.append('   MISSING IMAGE FILE: ' + m)
out.append('')
out.append('Total distinct missing referenced image paths: ' + str(len(missing_images_total)))
for m in sorted(missing_images_total):
    out.append(' - ' + m)

report_path = BASE / 'scripts' / 'light_audit_report.txt'
report_path.write_text('\n'.join(out), encoding='utf-8')
print('Wrote report to', report_path)
