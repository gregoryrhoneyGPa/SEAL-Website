"""
FORA PDF Travel Guides to Website Converter
Converts FORA travel guide PDFs to branded HTML pages for your website
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging
import re

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fora_pdf_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PDFConverter:
    """Converts FORA PDF guides to HTML"""
    
    def __init__(self, pdf_dir='c:\\Users\\grego\\Documents\\FORA\\Travel Guides'):
        self.pdf_dir = Path(pdf_dir)
        
        if not self.pdf_dir.exists():
            logger.warning(f"PDF directory not found: {pdf_dir}")
    
    def find_pdfs(self) -> List[Path]:
        """Find all PDF files in the directory"""
        if not self.pdf_dir.exists():
            return []
        
        pdfs = list(self.pdf_dir.glob('*.pdf'))
        logger.info(f"Found {len(pdfs)} PDF files")
        return pdfs
    
    def extract_text(self, pdf_path: Path) -> Optional[str]:
        """Extract text content from PDF"""
        if not PyPDF2:
            logger.error("PyPDF2 not installed. Run: pip install PyPDF2")
            return None
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = []
                
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
                
                full_text = '\n\n'.join(text)
                logger.info(f"✓ Extracted {len(full_text)} characters from {pdf_path.name}")
                return full_text
                
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path.name}: {str(e)}")
            return None
    
    def parse_guide_info(self, pdf_path: Path, text: str) -> Dict:
        """Parse guide information from filename and content"""
        # Get title from filename
        title = pdf_path.stem.replace('-', ' ').replace('_', ' ').title()
        
        # Try to extract location/destination
        location = self._extract_location(text)
        
        # Try to extract key highlights
        highlights = self._extract_highlights(text)
        
        guide = {
            'title': title,
            'filename': pdf_path.name,
            'location': location,
            'highlights': highlights,
            'text': text,
            'source_pdf': str(pdf_path),
            'converted_date': datetime.now().isoformat()
        }
        
        return guide
    
    def _extract_location(self, text: str) -> str:
        """Try to extract location from content"""
        # Look for common location patterns
        patterns = [
            r'(?:destination|location|country|region):\s*([^\n]+)',
            r'(?:visit|explore|discover)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ''
    
    def _extract_highlights(self, text: str) -> List[str]:
        """Extract key highlights or bullet points"""
        highlights = []
        
        # Look for bullet points or numbered lists
        lines = text.split('\n')
        for line in lines[:50]:  # Check first 50 lines
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or 
                        line.startswith('*') or re.match(r'^\d+\.', line)):
                highlight = re.sub(r'^[•\-*\d.]+\s*', '', line)
                if len(highlight) > 10:
                    highlights.append(highlight)
        
        return highlights[:5]  # Return top 5


class WebPublisher:
    """Publishes converted guides to website"""
    
    def __init__(self, output_dir='travel-guides'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.index_file = self.output_dir / 'index.json'
    
    def publish_guide(self, guide: Dict) -> bool:
        """Publish a guide to the website"""
        try:
            # Create sanitized filename
            safe_title = re.sub(r'[^\w\s-]', '', guide['title']).strip().replace(' ', '-')
            safe_title = safe_title[:50].lower()
            
            html_file = self.output_dir / f"{safe_title}.html"
            
            # Create HTML page
            html_content = self._create_html_page(guide)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Copy PDF to travel-guides folder for download
            pdf_copy = self.output_dir / guide['filename']
            if not pdf_copy.exists():
                import shutil
                shutil.copy2(guide['source_pdf'], pdf_copy)
            
            # Update index
            self._update_index(guide, str(html_file.name))
            
            logger.info(f"✓ Published: {guide['title']} → {html_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing guide: {str(e)}")
            return False
    
    def _create_html_page(self, guide: Dict) -> str:
        """Create branded HTML page"""
        
        # Format text into paragraphs
        text = guide['text']
        
        # Split into paragraphs (double line breaks)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Filter out very short paragraphs (likely formatting artifacts)
        paragraphs = [p for p in paragraphs if len(p) > 50]
        
        formatted_content = '\n'.join([f'<p>{p}</p>' for p in paragraphs])
        
        # Create highlights section
        highlights_html = ''
        if guide['highlights']:
            highlights_html = '<div class="highlights" style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 2rem 0;">'
            highlights_html += '<h3 style="color: #0b6fa4; margin-bottom: 1rem;">Key Highlights</h3>'
            highlights_html += '<ul style="list-style: none; padding: 0;">'
            for highlight in guide['highlights']:
                highlights_html += f'<li style="padding: 0.5rem 0; border-bottom: 1px solid #dee2e6;">✓ {highlight}</li>'
            highlights_html += '</ul></div>'
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Expert travel guide for {guide['title']} curated by SEAL Enterprises">
    <title>{guide['title']} - SEAL Enterprises Travel Guide</title>
    <link rel="stylesheet" href="../css/styles.css">
    <style>
        .travel-guide {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        .guide-header {{
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 2px solid #0b6fa4;
        }}
        .guide-header h1 {{
            color: #0b6fa4;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
            line-height: 1.2;
        }}
        .guide-content {{
            line-height: 1.8;
            font-size: 1.05rem;
            color: #333;
        }}
        .guide-content p {{
            margin-bottom: 1.5rem;
        }}
        .download-pdf {{
            background: #28a745;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            font-weight: 600;
            margin: 1rem 0;
        }}
        .download-pdf:hover {{
            background: #218838;
        }}
        .guide-footer {{
            margin-top: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            text-align: center;
        }}
        @media (max-width: 768px) {{
            .guide-header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <nav class="navbar" style="background: #0b6fa4; padding: 1rem 0; color: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; display: flex; justify-content: space-between; align-items: center;">
            <a href="../index.html" style="color: white; text-decoration: none; font-weight: 700; font-size: 1.2rem;">SEAL Enterprises</a>
            <a href="../index.html" style="color: white; text-decoration: none;">← Back to Home</a>
        </div>
    </nav>
    
    <main class="travel-guide">
        <article>
            <header class="guide-header">
                <h1>{guide['title']}</h1>
                {f'<p style="font-size: 1.2rem; color: #666; margin-top: 0.5rem;">📍 {guide["location"]}</p>' if guide['location'] else ''}
                <p style="font-size: 0.95rem; color: #999; margin-top: 0.5rem;">
                    Curated by Gregory Rhoney • SEAL Enterprises
                </p>
                <a href="{guide['filename']}" download class="download-pdf">
                    📥 Download PDF Guide
                </a>
            </header>
            
            {highlights_html}
            
            <div class="guide-content">
                {formatted_content}
            </div>
            
            <footer class="guide-footer">
                <h3 style="color: #0b6fa4; margin-bottom: 1rem;">Ready to Plan Your Trip?</h3>
                <p style="font-size: 1.05rem; color: #555; margin-bottom: 1rem;">
                    Let me help you create the perfect {guide['title']} experience with exclusive rates and VIP perks.
                </p>
                <a href="../contact.html" class="btn btn-primary" style="display: inline-block; background: #0b6fa4; color: white; padding: 0.75rem 2rem; border-radius: 4px; text-decoration: none; font-weight: 600; margin-top: 1rem;">
                    Contact Gregory Rhoney
                </a>
                
                <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #ddd;">
                    <p style="font-size: 0.85rem; color: #999;">
                        Travel guide content powered by FORA Travel<br>
                        Curated and personalized by SEAL Enterprises
                    </p>
                </div>
            </footer>
        </article>
    </main>
    
    <footer style="margin-top: 3rem; padding: 2rem 0; background: #f8f9fa; text-align: center;">
        <div class="container">
            <a href="https://www.foratravel.com/advisor/gregory-rhoney" target="_blank" rel="noopener noreferrer">
                <img src="../icons/Fora_Logo_Wordmark_Black-Sand_S.png" alt="Powered by FORA Travel" height="50" loading="lazy">
            </a>
            <p style="margin-top: 1rem; font-size: 0.9rem;">
                Proudly Powered by <a href="https://www.foratravel.com/advisor/gregory-rhoney" target="_blank" rel="noopener noreferrer" style="color: #0b6fa4; text-decoration: underline;">FORA Travel</a>
            </p>
        </div>
    </footer>
</body>
</html>"""
        return html_template
    
    def _update_index(self, guide: Dict, filename: str):
        """Update the guides index"""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            else:
                index = {'guides': [], 'last_updated': None}
            
            guide_entry = {
                'title': guide['title'],
                'filename': filename,
                'pdf_filename': guide['filename'],
                'location': guide['location'],
                'published_date': datetime.now().isoformat(),
                'source': 'FORA Travel'
            }
            
            # Remove existing entry with same filename
            index['guides'] = [g for g in index['guides'] if g['filename'] != filename]
            index['guides'].append(guide_entry)
            index['last_updated'] = datetime.now().isoformat()
            
            # Sort by title
            index['guides'].sort(key=lambda x: x['title'])
            
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error updating index: {str(e)}")


def main():
    """Main conversion process"""
    logger.info("=" * 70)
    logger.info("FORA PDF Travel Guides → Website Converter")
    logger.info("=" * 70)
    
    # Check for PyPDF2
    if not PyPDF2:
        logger.error("PyPDF2 is required. Installing...")
        os.system('pip install PyPDF2')
        logger.info("Please run the script again after installation completes.")
        return
    
    # Initialize
    converter = PDFConverter()
    publisher = WebPublisher()
    
    # Find PDFs
    logger.info("\nScanning for PDF files...")
    pdfs = converter.find_pdfs()
    
    if not pdfs:
        logger.error("No PDF files found.")
        logger.info("Please ensure PDFs are in: c:\\Users\\grego\\Documents\\FORA\\Travel Guides\\")
        return
    
    # Convert each PDF
    logger.info(f"\nConverting {len(pdfs)} PDF guides...")
    converted = 0
    
    for pdf_path in pdfs:
        logger.info(f"\n📄 Processing: {pdf_path.name}")
        
        # Extract text
        text = converter.extract_text(pdf_path)
        if not text:
            continue
        
        # Parse guide info
        guide = converter.parse_guide_info(pdf_path, text)
        
        # Publish to website
        if publisher.publish_guide(guide):
            converted += 1
    
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ Conversion Complete!")
    logger.info(f"   Converted: {converted}/{len(pdfs)} guides")
    logger.info(f"   Output: {publisher.output_dir.absolute()}")
    logger.info("=" * 70)
    
    if converted > 0:
        logger.info("\n📁 Check the 'travel-guides' folder for:")
        logger.info("   • HTML pages (for your website)")
        logger.info("   • PDF files (for download)")
        logger.info("   • index.json (catalog)")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nConversion interrupted by user")
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}", exc_info=True)
