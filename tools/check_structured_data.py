import re
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'Index.html'

def extract_jsonld(html_text):
    pattern = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S|re.I)
    return pattern.findall(html_text)

def validate_block(block_text):
    try:
        data = json.loads(block_text)
    except json.JSONDecodeError as e:
        return False, f'JSON decode error: {e}'

    if not isinstance(data, dict):
        return False, 'Top-level JSON-LD is not an object'

    ctx = data.get('@context')
    if not ctx or 'schema.org' not in ctx:
        return False, f'@context looks wrong: {ctx}'

    graph = data.get('@graph')
    if not graph or not isinstance(graph, list):
        return False, '@graph missing or not a list'

    errors = []
    for item in graph:
        t = item.get('@type')
        if t == 'Organization':
            _id = item.get('@id','')
            url = item.get('url','')
            logo = item.get('logo','')
            if not _id.startswith('https://sealenterprise.net'):
                errors.append(f'Organization @id not using production domain: {_id}')
            if not url.startswith('https://sealenterprise.net'):
                errors.append(f'Organization url not using production domain: {url}')
            if logo and not logo.startswith('https://sealenterprise.net'):
                errors.append(f'Organization logo not absolute production URL: {logo}')
        if t == 'WebSite':
            url = item.get('url','')
            if not url.startswith('https://sealenterprise.net'):
                errors.append(f'WebSite url not using production domain: {url}')
            pub = item.get('publisher',{})
            pid = pub.get('@id','') if isinstance(pub, dict) else ''
            if pid and not pid.startswith('https://sealenterprise.net'):
                errors.append(f'publisher @id not using production domain: {pid}')
        if t == 'ItemList':
            elems = item.get('itemListElement',[])
            for li in elems:
                url = li.get('url','')
                img = li.get('image','')
                if url and not url.startswith('https://sealenterprise.net'):
                    errors.append(f'ListItem url not using production domain: {url}')
                if img and not img.startswith('https://sealenterprise.net'):
                    errors.append(f'ListItem image not using production domain: {img}')

    if errors:
        return False, '\n'.join(errors)
    return True, 'OK'

def main():
    if not INDEX.exists():
        print('Index.html not found at', INDEX)
        sys.exit(2)

    html = INDEX.read_text(encoding='utf-8')
    blocks = extract_jsonld(html)
    if not blocks:
        print('No JSON-LD blocks found in Index.html')
        sys.exit(3)

    all_ok = True
    for i,b in enumerate(blocks,1):
        print(f'--- JSON-LD block #{i} ---')
        ok, msg = validate_block(b.strip())
        if ok:
            print('VALID:', msg)
        else:
            print('INVALID:', msg)
            all_ok = False

    if all_ok:
        print('\nAll checks passed.')
        sys.exit(0)
    else:
        print('\nOne or more checks failed.')
        sys.exit(4)

if __name__ == '__main__':
    main()
