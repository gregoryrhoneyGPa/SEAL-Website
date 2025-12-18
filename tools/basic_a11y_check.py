from html.parser import HTMLParser
from pathlib import Path
import sys


class A11yParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.title = ''
        self.in_title = False
        self.meta_description = None
        self.h1_count = 0
        self.imgs = []  # tuples (src, alt)
        self.inputs = []  # tuples (type, id, name, in_label)
        self.labels_for = set()
        self.in_label = False
        self.current_label_for = None
        self.label_nesting_inputs = []
        self.anchors = []  # tuples (href, text, aria-label)
        self.current_anchor = None
        self.saw_nav = False
        self.saw_header = False
        self.saw_main = False
        self.saw_footer = False
        self.buttons = []  # dicts

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.html_lang = attrs.get('lang')
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            name = attrs.get('name','').lower()
            if name == 'description':
                self.meta_description = attrs.get('content')
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'img':
            self.imgs.append((attrs.get('src',''), attrs.get('alt')))
        if tag == 'label':
            self.in_label = True
            self.current_label_for = attrs.get('for')
            if self.current_label_for:
                self.labels_for.add(self.current_label_for)
        if tag == 'input':
            itype = attrs.get('type','').lower()
            iid = attrs.get('id')
            iname = attrs.get('name')
            in_label = self.in_label
            self.inputs.append((itype, iid, iname, in_label))
        if tag == 'a':
            href = attrs.get('href','')
            aria = attrs.get('aria-label')
            self.current_anchor = {'href':href,'text':'','aria':aria}
        if tag == 'nav':
            self.saw_nav = True
        if tag == 'header':
            self.saw_header = True
        if tag == 'main':
            self.saw_main = True
        if tag == 'footer':
            self.saw_footer = True
        if tag == 'button':
            self.buttons.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'label':
            self.in_label = False
            self.current_label_for = None
        if tag == 'a' and self.current_anchor is not None:
            self.anchors.append(self.current_anchor)
            self.current_anchor = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        if self.current_anchor is not None:
            self.current_anchor['text'] += data


def run_checks(index_path: Path):
    if not index_path.exists():
        print('Index.html not found at', index_path)
        return 2

    parser = A11yParser()
    text = index_path.read_text(encoding='utf-8')
    parser.feed(text)

    issues = []

    if not parser.html_lang:
        issues.append('Missing lang attribute on <html>')

    if not parser.title:
        issues.append('Missing or empty <title>')

    if not parser.meta_description:
        issues.append('Missing meta description')

    if parser.h1_count == 0:
        issues.append('No <h1> found')
    elif parser.h1_count > 1:
        issues.append(f'Multiple <h1> elements found ({parser.h1_count}) — consider using a single H1')

    # images
    imgs_missing_alt = [src for (src,alt) in parser.imgs if alt is None or alt.strip()== '']
    if imgs_missing_alt:
        issues.append(f'Images missing alt text: {len(imgs_missing_alt)} (examples: {imgs_missing_alt[:5]})')

    # inputs and labels
    unlabeled_inputs = []
    for itype, iid, iname, in_label in parser.inputs:
        if itype in ('hidden','submit','button'):
            continue
        labeled = False
        if iid and iid in parser.labels_for:
            labeled = True
        if in_label:
            labeled = True
        if not labeled:
            unlabeled_inputs.append((itype,iid,iname))
    if unlabeled_inputs:
        issues.append(f'Form inputs without labels or associated label: {len(unlabeled_inputs)} (examples: {unlabeled_inputs[:5]})')

    # anchors
    anchors_without_text = [a['href'] for a in parser.anchors if (not a['text'].strip()) and not a['aria']]
    if anchors_without_text:
        issues.append(f'Links with no text or aria-label: {len(anchors_without_text)} (examples: {anchors_without_text[:5]})')

    # landmarks
    if not (parser.saw_header and parser.saw_main and parser.saw_footer):
        missing = []
        if not parser.saw_header: missing.append('header')
        if not parser.saw_main: missing.append('main')
        if not parser.saw_footer: missing.append('footer')
        issues.append('Missing semantic landmark elements: ' + ', '.join(missing))

    # nav-toggle button aria
    nav_toggle_issues = []
    for b in parser.buttons:
        cls = b.get('class','')
        if 'nav-toggle' in cls or b.get('id','').lower().find('nav')>=0:
            if 'aria-controls' not in b:
                nav_toggle_issues.append('nav toggle missing aria-controls')
            if 'aria-expanded' not in b:
                nav_toggle_issues.append('nav toggle missing aria-expanded')
    if nav_toggle_issues:
        issues.extend(nav_toggle_issues)

    # report
    print('Accessibility quick-check results for', index_path)
    print('-----------------------------------------------')
    if not issues:
        print('No obvious issues found by basic checks.')
        return 0
    print('Issues found:')
    for it in issues:
        print('- ', it)
    return 1


def main():
    root = Path(__file__).resolve().parents[1]
    index = root / 'Index.html'
    code = run_checks(index)
    sys.exit(code)


if __name__ == '__main__':
    main()
