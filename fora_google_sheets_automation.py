"""
FORA Travel Guides - Google Sheets Automation
Automatically pulls FORA "magic" content from Google Sheets and publishes to your website
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging
import re
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fora_guides_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration"""
    
    def __init__(self, config_file='fora_guides_config.txt'):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            logger.warning(f"Configuration file not found: {self.config_file}")
            logger.info("Using default settings. Create fora_guides_config.txt to customize.")
            return
        
        with open(self.config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
        
        logger.info("Configuration loaded successfully")
        return self.config
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)


class GoogleSheetsReader:
    """Reads FORA guides from exported Google Sheets CSV"""
    
    def __init__(self, csv_file='fora_guides.csv', advisor_id='gregory-rhoney'):
        self.csv_file = csv_file
        self.advisor_id = advisor_id
    
    def read_guides(self) -> List[Dict]:
        """Read travel guides from CSV export"""
        if not os.path.exists(self.csv_file):
            logger.error(f"CSV file not found: {self.csv_file}")
            logger.info("Please export your FORA Google Sheet as CSV and save it as 'fora_guides.csv'")
            return []
        
        guides = []
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Skip empty rows or rows without magic content
                    magic_content = row.get('Magic Content', '').strip()
                    if not magic_content:
                        continue
                    
                    # Personalize the URL with advisor ID
                    magic_url = self._personalize_url(magic_content)
                    
                    guide = {
                        'date': row.get('Date', ''),
                        'name': row.get('Name', ''),
                        'description': row.get('Description', ''),
                        'continent': row.get('Continent', ''),
                        'country': row.get('Country', '').strip(),
                        'region': row.get('Region', '').strip(),
                        'partner': row.get('Partner', ''),
                        'style': row.get('Style', ''),
                        'season': row.get('Season', ''),
                        'budget_friendly': row.get('< $500 option(s)', '').lower() in ['yes', 'true', 'x'],
                        'magic_content_url': magic_url,
                        'magic_content_original': magic_content,
                        'instagram_feed': row.get('Instagram In-Feed', ''),
                        'instagram_story': row.get('Instagram Story', ''),
                        'video_template': row.get('Video Template', ''),
                        'pdf_template': row.get('PDF Template', ''),
                        'notes': row.get('Notes', ''),
                        'article_title': row.get('Article Title (Fora HQ reference)', '')
                    }
                    
                    guides.append(guide)
            
            logger.info(f"✓ Loaded {len(guides)} travel guides from CSV")
            return guides
            
        except Exception as e:
            logger.error(f"Error reading CSV: {str(e)}")
            return []
    
    def _personalize_url(self, url: str) -> str:
        """Add advisor ID to FORA URL to personalize it"""
        if not url or not url.startswith('http'):
            return url
        
        # If URL already contains the advisor ID, return as-is
        if self.advisor_id in url:
            return url
        
        # Add advisor ID to the URL path
        # Example: https://foratravel.com/content/article → https://foratravel.com/advisor/gregory-rhoney/content/article
        if '/advisor/' not in url:
            # Find where to insert the advisor path
            parts = url.split('/')
            if len(parts) >= 4:  # https://domain.com/path
                # Insert advisor path after domain
                base = '/'.join(parts[:3])  # https://domain.com
                path = '/'.join(parts[3:])   # rest of path
                return f"{base}/advisor/{self.advisor_id}/{path}"
        
        return url
FORAContentFetcher:
    """Fetches content from FORA magic content URLs"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.session = requests.Session()
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """Authenticate with FORA portal"""
        username = self.config.get('FORA_USERNAME')
        password = self.config.get('FORA_PASSWORD')
        
        if not username or not password or username.startswith('your-'):
            logger.warning("FORA credentials not configured - will attempt to fetch without authentication")
            return False
        
        try:
            logger.info(f"Authenticating with FORA as {username}...")
            
            # FORA login URL
            login_url = 'https://www.foratravel.com/login'
            
            # Get login page first
            response = self.session.get(login_url, timeout=10)
            
            # Attempt login
            login_data = {
                'email': username,
                'password': password
            }
            
            auth_response = self.session.post(login_url, data=login_data, timeout=10)
            
            if auth_response.status_code in [200, 302]:
                self.authenticated = True
                logger.info("✓ Successfully authenticated with FORA")
                return True
            else:
                logger.warning("Authentication may have failed")
                return False, fetched_content: Optional[str] = None) -> str:
        """Create a complete branded HTML page"""
        
        # Use fetched content if available, otherwise use placeholder
        if fetched_content:
            formatted_content = fetched_content
        else:
            # Fallback: create a preview/teaser page
            formatted_content = f"""
            <div style="padding: 2rem; background: #f8f9fa; border-radius: 8px; text-align: center;">
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">
                    This travel guide is available exclusively through FORA Travel.
                </p>
                <p style="margin-bottom: 1.5rem;">
                    <a href="{guide.get('magic_content_url', '')}" 
                       target="_blank" 
                       rel="noopener noreferrer"
                       class="btn"
                       style="display: inline-block; background: #0b6fa4; color: white; padding: 0.75rem 2rem; 
                              border-radius: 4px; text-decoration: none; font-weight: 600;">
                        View Full Guide on FORA
                    </a>
                </p>
                <p style="font-size: 0.9rem; color: #666;">
                    Contact me for personalized assistance with this destination.
                </p>
            </div>
            """
                # Extract the main article content
                content = self._extract_article_content(soup)
                
                if content:
                    logger.info("✓ Content fetched successfully")
                    return content
                else:
                    logger.warning("Could not extract article content from page")
                    return None
            else:
                logger.warning(f"Failed to fetch content: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching content: {str(e)}")
            return None
    
    def _extract_article_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article content from FORA page"""
        # Try multiple selectors for FORA's content structure
        content_selectors = [
            {'name': 'article', 'class': re.compile(r'.*content.*|.*article.*|.*post.*')},
            {'name': 'div', 'class': re.compile(r'.*content.*|.*article.*|.*post.*')},
            {'name': 'main'},
            {'name': 'article'}
        ]
        
        for selector in content_selectors:
            if 'class' in selector:
                content_div = soup.find(selector['name'], class_=selector['class'])
            else:
                content_div = soup.find(selector['name'])
            
            if content_div:
                # Clean up the content
                for tag in content_div(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    tag.decompose()
                
                # Get text content with basic formatting
                content_html = str(content_div)
                
                # Return if we found substantial content
                if len(content_html) > 200:
                    return content_html
        
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs and len(paragraphs) > 3:
            content_html = '\n'.join([str(p) for p in paragraphs])
            return content_html
        
        return None


class ContentPublisher:
    """Publishes travel guides to website"""
    
    def __init__(self, output_dir='travel-guides'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.index_file = self.output_dir / 'index.json'
        self.state_file = Path('published_guides_state.json')
    
    def publish_guide(self, guide: Dict, fetched_content: Optional[str] = Noneed_guides_state.json')
    
    def publish_guide(self, guide: Dict) -> bool:
        """Publish a travel guide to the website"""
        try:
            # Create sanitized filename from name
            safe_title = re.sub(r'[^\w\s-]', '', guide['name']).strip().replace(' ', '-')
            safe_title = safe_title[:50].lower()  # Limit length
            
            if not safe_title:
                safe_title = f"guide-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Save HTML file
            html_file = self.output_dir / f"{safe_title}.html"
            
            # Create branded HTML content
            html_content = self._create_html_page(guide)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Update index
            self._update_index(guide, str(html_file.name))
            
            logger.info(f"✓ Published guide: {guide['name']} → {html_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing guide '{guide.get('name', 'Unknown')}': {str(e)}")
            return False
    
    def _create_html_page(self, guide: Dict) -> str:
        """Create a complete branded HTML page"""
        
        # Process magic content - convert line breaks to paragraphs
        content = guide['magic_content'].strip()
        
        # If content has URLs, make them clickable
        content = re.sub(
            r'(https?://[^\s<>"]+)',
            r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>',
            content
        )
        
        # Split into paragraphs on double line breaks
        paragraphs = content.split('\n\n')
        formatted_content = '\n'.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])
        
        # Create location string
        location_parts = [guide['region'], guide['country'], guide['continent']]
        location = ', '.join([part for part in location_parts if part])
        
        # Budget badge
        budget_badge = ''
        if guide['budget_friendly']:
            budget_badge = '<span class="budget-badge" style="background: #28a745; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.85rem; font-weight: 600;">Budget-Friendly Options Available</span>'
        
        # Tags
        tags = []
        if guide['style']:
            tags.append(guide['style'])
        if guide['season']:
            tags.append(guide['season'])
        if guide['partner']:
            tags.append(f"Partner: {guide['partner']}")
        
        tags_html = ''
        if tags:
            tags_html = '<div class="guide-tags" style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem;">'
            for tag in tags:
                tags_html += f'<span style="background: #e9ecef; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.85rem;">{tag}</span>'
            tags_html += '</div>'
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{guide['description'][:155]}">
    <title>{guide['name']} - SEAL Enterprises Travel Guide</title>
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
        .guide-meta {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
            color: #666;
            font-size: 0.95rem;
            margin-top: 1rem;
        }}
        .guide-content {{
            line-height: 1.8;
            font-size: 1.1rem;
            color: #333;
        }}
        .guide-content p {{
            margin-bottom: 1.5rem;
        }}
        .guide-content a {{
            color: #0b6fa4;
            text-decoration: underline;
        }}
        .guide-footer {{
            margin-top: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            text-align: center;
        }}
        .guide-footer h3 {{
            color: #0b6fa4;
            margin-bottom: 1rem;
        }}
        .btn {{
            display: inline-block;
            background: #0b6fa4;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.2s;
            margin-top: 1rem;
        }}
        .btn:hover {{
            background: #094d73;
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
            <a href="../index.html" style="color
            advisor_id=self.config.get('FORA_ADVISOR_ID', 'gregory-rhoney')
        )
        self.content_fetcher = FORAContentFetcher(self.config: white; text-decoration: none; font-weight: 700; font-size: 1.2rem;">SEAL Enterprises</a>
            <a href="../index.html" style="color: white; text-decoration: none;">← Back to Home</a>
        </div>
    </nav>
    
    <main class="travel-guide">
        <article>
            <header class="guide-header">
                <h1>{guide['name']}</h1>
                
                <div class="guide-meta">
                    {f'<span>📍 {location}</span>' if location else ''}
                    {f'<span>📅 {guide["date"]}</span>' if guide['date'] else ''}
                    {budget_badge}
                </div>
                
                {f'<p style="font-size: 1.15rem; color: #555; margin-top: 1rem; font-style: italic;">{guide["description"]}</p>' if guide['description'] else ''}
                
                {tags_html}
            </header>
            
            <div class="guide-content">
                {formatted_content}
            </div>
            
            <footer class="guide-footer">
                <h3>Ready to Experience {guide['country'] or 'This Destination'}?</h3>
                <p style="font-size: 1.05rem; color: #555; margin-bottom: 0.5rem;">
                    Let me help you plan the perfect trip with exclusive rates and VIP perks.
                </p>
                <p style="font-size: 0.95rem; color: #666;">
                    As a FORA Travel advisor, I provide personalized service and insider access.
                </p>
                <a href="../contact.html" class="btn">Contact Gregory Rhoney</a>
                
                <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #ddd;">
                    <p style="font-size: 0.85rem; color: #999;">
                        Travel guide curated by SEAL Enterprises<br>
                        Content powered by FORA Travel
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
        """Update the guides index file"""
        try:
            # Load existing index
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            else:
                index = {'guides': [], 'last_updated': None}
            
            # Add or update guide entry
            guide_entry = {
                'title': guide['name'],
                'description': guide['description'],
                'filename': filename,
                'location': f"{guide['region']}, {guide['country']}" if guide['country'] else guide['continent'],
                'continent': guide['continent'],
                'country': guide['country'],
                'style': guide['style'],
                'season': guide['season'],
                'budget_friendly': guide['budget_friendly'],
                'published_date': datetime.now().isoformat(),
                'source': 'FORA Travel'
            }
            
            # Remove any existing entry with same filename
            index['guides'] = [g for g in index['guides'] if g['filename'] != filename]
            index['guides'].append(guide_entry)
            index['last_updated'] = datetime.now().isoformat()
            
            # Sort by published date (newest first)
            index['guides'].sort(key=lambda x: x['published_date'], reverse=True)
            
            # Save updated index
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating index: {str(e)}")
    
    def load_published_state(self) -> List[str]:
        """Load list of already published guide names"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                return state.get('published_guides', [])
        return []
    
    def save_published_state(self, published_guides: List[str]):
        """Save list of published guide names"""
        state = {
            'published_guides': published_guides,
            'last_run': datetime.now().isoformat()
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)


class AutomationManager:
    """Main automation orchestrator"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.sheets_reader = GoogleSheetsReader()
        self.publisher = ContentPublisher()
    
    def run(self):
        ""Authenticate with FORA if credentials are provided
        fetch_content = self.config.get('FETCH_FORA_CONTENT', 'True') == 'True'
        
        if fetch_content:
            logger.info("\nAuthenticating with FORA...")
            if not self.content_fetcher.authenticate():
                logger.warning("Continuing without FORA authentication - will create preview pages only")
                fetch_content = False
        else:
            logger.info("Content fetching disabled - will create preview pages with links")
        
        # Load previous state to avoid republishing
        published_guides = self.publisher.load_published_state()
        logger.info(f"Previously published: {len(published_guides)} guides")
        
        # Process each guide
        new_count = 0
        skipped_count = 0
        
        for guide in guides:
            guide_id = guide['name']
            
            if guide_id in published_guides:
                skipped_count += 1
                logger.debug(f"Skipping already published: {guide['name']}")
                continue
            
            logger.info(f"\n📚 Processing: {guide['name']}")
            
            # Fetch content from FORA if enabled
            fetched_content = None
            if fetch_content and guide.get('magic_content_url'):
                fetched_content = self.content_fetcher.fetch_content(guide['magic_content_url'])
            
            # Publish to website
            if self.publisher.publish_guide(guide, fetched_content
        new_count = 0
        skipped_count = 0
        
        for guide in guides:
            guide_id = guide['name']
            
            if guide_id in published_guides:
                skipped_count += 1
                logger.debug(f"Skipping already published: {guide['name']}")
                continue
            
            logger.info(f"\n📚 Processing: {guide['name']}")
            
            # Publish to website
            if self.publisher.publish_guide(guide):
                published_guides.append(guide_id)
                new_count += 1
        
        # Save state
        self.publisher.save_published_state(published_guides)
        
        logger.info("\n" + "=" * 70)
        logger.info(f"Automation Complete!")
        logger.info(f"  New guides published: {new_count}")
        logger.info(f"  Previously published (skipped): {skipped_count}")
        logger.info(f"  Total guides in catalog: {len(published_guides)}")
        logger.info(f"  Output directory: {self.publisher.output_dir.absolute()}")
        logger.info("=" * 70)
        
        if new_count > 0:
            logger.info("\n✓ Check the 'travel-guides' folder for your new HTML files!")
            logger.info("✓ View 'travel-guides/index.json' for the complete catalog")


if __name__ == '__main__':
    try:
        automation = AutomationManager()
        automation.run()
    except KeyboardInterrupt:
        logger.info("\nAutomation interrupted by user")
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}", exc_info=True)
