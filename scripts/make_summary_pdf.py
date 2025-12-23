from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.units import inch
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = [
    os.path.join(ROOT, 'EXPORT_WORK_SUMMARY_2025-12-17.txt'),
    os.path.join(ROOT, 'EXPORT_FULL_2025-12-17.txt'),
]

out_pdf = os.path.join(ROOT, 'EXPORT_SUMMARIES_2025-12-17_18.pdf')

doc = SimpleDocTemplate(out_pdf, pagesize=letter, rightMargin=36,leftMargin=36, topMargin=36,bottomMargin=36)
styles = getSampleStyleSheet()
style_h = styles['Heading2']
style_mono = styles.get('Code', styles['BodyText'])

elements = []
for path in files:
    if not os.path.exists(path):
        elements.append(Paragraph(f'File not found: {os.path.basename(path)}', style_h))
        elements.append(Spacer(1, 12))
        continue
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read().strip()
    elements.append(Paragraph(os.path.basename(path), style_h))
    elements.append(Spacer(1, 6))
    elements.append(Preformatted(text, style_mono))
    elements.append(PageBreak())

if not elements:
    print('No content to write.')
else:
    doc.build(elements)
    print(f'Wrote PDF: {out_pdf}')
