"""
FORA URL Extractor
Extracts actual magic URLs from FORA Google Sheet CSV and adds advisor tracking
"""

import csv
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def extract_fora_urls(csv_file='fora_guides.csv', advisor_id='gregory-rhoney'):
    """Extract magic content URLs and add advisor tracking"""
    
    if not os.path.exists(csv_file):
        logger.error(f"CSV not found: {csv_file}")
        return []
    
    guides_with_urls = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            # Skip first line if not header
            first_line = f.readline()
            if 'Date' not in first_line and 'Name' not in first_line:
                f.seek(0)
                f.readline()
            else:
                f.seek(0)
            
            reader = csv.DictReader(f)
            
            for row in reader:
                name = row.get('Name', '').strip()
                if not name:
                    continue
                
                # Check if there's a URL in the Magic Content column
                magic_url = row.get('Magic Content', '').strip()
                
                # Only include if there's an actual URL (starts with http)
                if magic_url and magic_url.startswith('http'):
                    # Ensure advisor ID is in the URL
                    if advisor_id not in magic_url:
                        # Add advisor parameter
                        separator = '&' if '?' in magic_url else '?'
                        magic_url = f"{magic_url}{separator}advisor={advisor_id}"
                    
                    guides_with_urls.append({
                        'name': name,
                        'url': magic_url,
                        'continent': row.get('Continent', 'Other').strip(),
                        'description': row.get('Short Description', '').strip()
                    })
        
        logger.info(f"Found {len(guides_with_urls)} guides with valid URLs")
        return guides_with_urls
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return []


def save_url_catalog(guides, output_file='fora_urls_catalog.json'):
    """Save the URLs catalog"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_guides': len(guides),
            'advisor_id': 'gregory-rhoney',
            'guides': guides
        }, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved to {output_file}")


def main():
    logger.info("Extracting FORA URLs with advisor tracking...")
    guides = extract_fora_urls()
    
    if guides:
        save_url_catalog(guides)
        logger.info(f"\nFound {len(guides)} guides with valid URLs")
        logger.info(f"All URLs include advisor ID: gregory-rhoney")
        
        # Show first few examples
        logger.info("\nSample URLs:")
        for guide in guides[:3]:
            logger.info(f"  {guide['name']}")
            logger.info(f"    {guide['url'][:80]}...")
    else:
        logger.warning("No guides with valid URLs found")
        logger.info("The 'Magic Content' column may contain text instead of URLs")


if __name__ == '__main__':
    main()
