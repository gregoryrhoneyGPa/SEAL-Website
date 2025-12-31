"""
FORA PDF Branding Tool
Adds SEAL Enterprises branding/contact info to FORA PDFs
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
import io
import os


def create_branding_overlay():
    """Create a PDF overlay with your branding"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Add footer with your contact info
    can.setFillColor(HexColor('#0b6fa4'))
    can.setFont("Helvetica-Bold", 10)
    
    # Bottom of page
    can.drawString(50, 30, "Curated by Gregory Rhoney | SEAL Enterprises")
    can.setFont("Helvetica", 9)
    can.drawString(50, 18, "📧 Contact: gregory.rhoney@sealenterprises.net | 🌐 www.sealenterprises.net")
    
    can.save()
    packet.seek(0)
    return PdfReader(packet)


def add_branding_to_pdf(input_pdf, output_pdf):
    """Add your branding to a FORA PDF"""
    
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found")
        return False
    
    try:
        # Read original PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        # Create branding overlay
        branding = create_branding_overlay()
        branding_page = branding.pages[0]
        
        # Add branding to each page
        for page in reader.pages:
            page.merge_page(branding_page)
            writer.add_page(page)
        
        # Add metadata
        writer.add_metadata({
            '/Author': 'Gregory Rhoney - SEAL Enterprises',
            '/Title': f'Travel Guide - Curated by SEAL Enterprises',
            '/Subject': 'Destination Travel Guide',
            '/Creator': 'SEAL Enterprises Travel Planning'
        })
        
        # Write output
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"✓ Branded PDF created: {output_pdf}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def brand_all_guides(guides_dir='guides'):
    """Brand all PDFs in guides directory"""
    
    if not os.path.exists(guides_dir):
        print(f"Creating {guides_dir} directory...")
        os.makedirs(guides_dir)
        return
    
    pdf_files = [f for f in os.listdir(guides_dir) if f.endswith('.pdf') and not f.startswith('branded-')]
    
    if not pdf_files:
        print(f"No PDFs found in {guides_dir}/")
        print("Download FORA PDFs and place them there first.")
        return
    
    print(f"Found {len(pdf_files)} PDF(s) to brand\n")
    
    for pdf_file in pdf_files:
        input_path = os.path.join(guides_dir, pdf_file)
        output_path = os.path.join(guides_dir, f'branded-{pdf_file}')
        
        print(f"Branding: {pdf_file}")
        add_branding_to_pdf(input_path, output_path)
    
    print(f"\n✓ Done! Branded PDFs saved with 'branded-' prefix")
    print(f"Send the branded versions to clients!")


if __name__ == '__main__':
    print("=" * 60)
    print("FORA PDF Branding Tool")
    print("=" * 60)
    print()
    
    # Check if PyPDF2 is installed
    try:
        import PyPDF2
        import reportlab
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'PyPDF2', 'reportlab'])
        print("Packages installed. Please run this script again.")
        exit()
    
    brand_all_guides()
