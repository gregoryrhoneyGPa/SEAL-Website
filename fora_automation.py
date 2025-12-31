"""
FORA Travel Guides & Mailchimp Automation System
Automatically fetches FORA "magic" travel guides and integrates with Mailchimp
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging
from bs4 import BeautifulSoup
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fora_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration and credentials with validation"""
    
    def __init__(self, config_file='fora_config.txt'):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            logger.error(f"Configuration file not found: {self.config_file}")
            logger.info("Please copy fora_config.txt.template to fora_config.txt and fill in your credentials")
            raise FileNotFoundError(f"Missing {self.config_file}")
        
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
    
    def validate_credentials(self) -> bool:
        """Validate that all required credentials are present"""
        required = ['FORA_USERNAME', 'FORA_PASSWORD', 'MAILCHIMP_API_KEY', 'MAILCHIMP_LIST_ID']
        missing = [key for key in required if not self.get(key) or self.get(key).startswith('your-')]
        
        if missing:
            logger.warning(f"Missing or incomplete credentials: {', '.join(missing)}")
            return False
        return True


class FORAClient:
    """Handles FORA authentication and content fetching"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.session = requests.Session()
        self.authenticated = False
        self.last_auth_check = None
    
    def authenticate(self) -> bool:
        """Authenticate with FORA portal"""
        try:
            login_url = self.config.get('FORA_LOGIN_URL')
            username = self.config.get('FORA_USERNAME')
            password = self.config.get('FORA_PASSWORD')
            
            logger.info(f"Authenticating with FORA as {username}...")
            
            # First, get the login page to extract any CSRF tokens or form fields
            response = self.session.get(login_url, timeout=10)
            
            if response.status_code == 200:
                # Parse the page for form fields if needed
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Attempt login (adjust payload based on actual FORA form structure)
                login_data = {
                    'username': username,
                    'email': username,  # Some sites use email
                    'password': password
                }
                
                # Post login
                auth_response = self.session.post(login_url, data=login_data, timeout=10)
                
                # Check if authenticated (adjust based on FORA's response)
                if auth_response.status_code in [200, 302] and 'logout' in auth_response.text.lower():
                    self.authenticated = True
                    self.last_auth_check = datetime.now()
                    logger.info("✓ Successfully authenticated with FORA")
                    return True
                else:
                    logger.warning("Authentication may have failed - please verify credentials")
                    return False
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def check_auth_validity(self) -> bool:
        """Check if current authentication is still valid"""
        if not self.authenticated:
            return False
        
        # Re-authenticate every 24 hours or if last check is None
        if not self.last_auth_check or \
           (datetime.now() - self.last_auth_check) > timedelta(hours=24):
            logger.info("Re-validating authentication...")
            return self.authenticate()
        
        return True
    
    def fetch_travel_guides(self) -> List[Dict]:
        """Fetch available travel guides from FORA"""
        if not self.check_auth_validity():
            if not self.authenticate():
                logger.error("Cannot fetch guides - authentication failed")
                return []
        
        try:
            guides_url = self.config.get('FORA_MAGIC_GUIDES_URL')
            logger.info(f"Fetching travel guides from {guides_url}...")
            
            response = self.session.get(guides_url, timeout=10)
            
            if response.status_code == 200:
                guides = self._parse_guides(response.text)
                logger.info(f"✓ Found {len(guides)} travel guides")
                return guides
            else:
                logger.warning(f"Failed to fetch guides: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching guides: {str(e)}")
            return []
    
    def _parse_guides(self, html: str) -> List[Dict]:
        """Parse travel guides from HTML response"""
        guides = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # This will need to be customized based on FORA's actual HTML structure
        # Looking for guide listings, titles, descriptions, URLs, etc.
        
        # Example parsing (adjust selectors based on actual FORA structure):
        guide_elements = soup.find_all(['article', 'div'], class_=re.compile(r'guide|resource|magic'))
        
        for element in guide_elements:
            try:
                title = element.find(['h2', 'h3', 'h4'])
                description = element.find(['p', 'div'], class_=re.compile(r'description|excerpt'))
                link = element.find('a', href=True)
                
                if title and link:
                    guide = {
                        'title': title.get_text(strip=True),
                        'description': description.get_text(strip=True) if description else '',
                        'url': link['href'],
                        'fetched_date': datetime.now().isoformat(),
                        'published': False
                    }
                    guides.append(guide)
            except Exception as e:
                logger.debug(f"Error parsing guide element: {str(e)}")
                continue
        
        return guides
    
    def download_guide_content(self, guide_url: str) -> Optional[Dict]:
        """Download full content of a specific travel guide"""
        if not self.check_auth_validity():
            if not self.authenticate():
                return None
        
        try:
            response = self.session.get(guide_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract main content
                content = {
                    'html': response.text,
                    'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else '',
                    'content': self._extract_main_content(soup),
                    'images': self._extract_images(soup),
                    'download_date': datetime.now().isoformat()
                }
                
                return content
                
        except Exception as e:
            logger.error(f"Error downloading guide content: {str(e)}")
            return None
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find main content area
        main_content = soup.find(['article', 'main', 'div'], class_=re.compile(r'content|article|post'))
        
        if main_content:
            return str(main_content)
        return str(soup.body) if soup.body else ''
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract image URLs from content"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                images.append(src)
        return images


class MailchimpClient:
    """Handles Mailchimp API interactions"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.api_key = config.get('MAILCHIMP_API_KEY')
        self.server = config.get('MAILCHIMP_SERVER_PREFIX', 'us21')
        self.list_id = config.get('MAILCHIMP_LIST_ID')
        self.base_url = f"https://{self.server}.api.mailchimp.com/3.0"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """Test Mailchimp API connection"""
        try:
            response = requests.get(f"{self.base_url}/ping", headers=self.headers, timeout=10)
            if response.status_code == 200:
                logger.info("✓ Mailchimp connection successful")
                return True
            else:
                logger.error(f"Mailchimp connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Mailchimp connection error: {str(e)}")
            return False
    
    def create_campaign(self, guide: Dict, content: str) -> Optional[str]:
        """Create a Mailchimp campaign from a travel guide"""
        try:
            campaign_data = {
                "type": "regular",
                "recipients": {
                    "list_id": self.list_id
                },
                "settings": {
                    "subject_line": f"New Travel Guide: {guide['title']}",
                    "preview_text": guide.get('description', '')[:150],
                    "title": f"SEAL - {guide['title']} - {datetime.now().strftime('%Y-%m-%d')}",
                    "from_name": "SEAL Enterprises",
                    "reply_to": self.config.get('FORA_USERNAME', 'gregory.rhoney@gmail.com')
                }
            }
            
            response = requests.post(
                f"{self.base_url}/campaigns",
                headers=self.headers,
                json=campaign_data,
                timeout=15
            )
            
            if response.status_code == 200:
                campaign = response.json()
                campaign_id = campaign['id']
                logger.info(f"✓ Created campaign: {campaign_id}")
                
                # Set campaign content
                self._set_campaign_content(campaign_id, content)
                
                return campaign_id
            else:
                logger.error(f"Failed to create campaign: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            return None
    
    def _set_campaign_content(self, campaign_id: str, html_content: str):
        """Set HTML content for a campaign"""
        try:
            content_data = {
                "html": html_content
            }
            
            response = requests.put(
                f"{self.base_url}/campaigns/{campaign_id}/content",
                headers=self.headers,
                json=content_data,
                timeout=15
            )
            
            if response.status_code == 200:
                logger.info(f"✓ Set content for campaign {campaign_id}")
                return True
            else:
                logger.error(f"Failed to set campaign content: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting campaign content: {str(e)}")
            return False
    
    def send_campaign(self, campaign_id: str) -> bool:
        """Send a campaign immediately"""
        try:
            response = requests.post(
                f"{self.base_url}/campaigns/{campaign_id}/actions/send",
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code == 204:
                logger.info(f"✓ Campaign {campaign_id} sent successfully")
                return True
            else:
                logger.error(f"Failed to send campaign: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending campaign: {str(e)}")
            return False


class ContentPublisher:
    """Publishes travel guides to website"""
    
    def __init__(self, output_dir='travel-guides'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.index_file = self.output_dir / 'index.json'
    
    def publish_guide(self, guide: Dict, content: Dict) -> bool:
        """Publish a travel guide to the website"""
        try:
            # Create sanitized filename
            safe_title = re.sub(r'[^\w\s-]', '', guide['title']).strip().replace(' ', '-')
            safe_title = safe_title[:50]  # Limit length
            
            # Save HTML file
            html_file = self.output_dir / f"{safe_title}.html"
            
            # Rebrand content with SEAL branding
            rebranded_content = self._rebrand_content(content, guide['title'])
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(rebranded_content)
            
            # Update index
            self._update_index(guide, str(html_file.name))
            
            logger.info(f"✓ Published guide: {html_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing guide: {str(e)}")
            return False
    
    def _rebrand_content(self, content: Dict, title: str) -> str:
        """Rebrand FORA content with SEAL branding"""
        # Create a complete HTML page with SEAL branding
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - SEAL Enterprises</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="../index.html" class="logo">SEAL Enterprises</a>
            <a href="../index.html">← Back to Home</a>
        </div>
    </nav>
    
    <main class="container" style="margin-top: 2rem;">
        <article class="travel-guide">
            <header>
                <h1>{title}</h1>
                <p class="byline">Curated by SEAL Enterprises | Powered by FORA Travel</p>
                <p class="publish-date">Published: {datetime.now().strftime('%B %d, %Y')}</p>
            </header>
            
            <div class="guide-content">
                {content.get('content', '')}
            </div>
            
            <footer class="guide-footer">
                <p><strong>Ready to book this experience?</strong></p>
                <a href="../contact.html" class="btn btn-primary">Contact Gregory Rhoney</a>
                <p style="margin-top: 1rem; font-size: 0.9rem;">
                    As your FORA Travel advisor, I provide exclusive rates, VIP perks, and personalized service.
                </p>
            </footer>
        </article>
    </main>
    
    <footer style="margin-top: 3rem; padding: 2rem 0; background: #f8f9fa; text-align: center;">
        <div class="container">
            <a href="https://www.foratravel.com/advisor/gregory-rhoney" target="_blank" rel="noopener noreferrer">
                <img src="../icons/Fora_Logo_Wordmark_Black-Sand_S.png" alt="Powered by FORA Travel" height="50" loading="lazy">
            </a>
            <p style="margin-top: 1rem;">Proudly Powered by <a href="https://www.foratravel.com/advisor/gregory-rhoney">FORA Travel</a></p>
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
                with open(self.index_file, 'r') as f:
                    index = json.load(f)
            else:
                index = {'guides': []}
            
            # Add or update guide entry
            guide_entry = {
                'title': guide['title'],
                'description': guide.get('description', ''),
                'filename': filename,
                'url': guide.get('url', ''),
                'published_date': datetime.now().isoformat(),
                'source': 'FORA Travel'
            }
            
            # Remove any existing entry with same filename
            index['guides'] = [g for g in index['guides'] if g['filename'] != filename]
            index['guides'].append(guide_entry)
            
            # Save updated index
            with open(self.index_file, 'w') as f:
                json.dump(index, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error updating index: {str(e)}")


class AutomationManager:
    """Main automation orchestrator"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.fora = FORAClient(self.config)
        self.mailchimp = MailchimpClient(self.config)
        self.publisher = ContentPublisher()
        self.state_file = Path('automation_state.json')
    
    def run(self):
        """Run the automation workflow"""
        logger.info("=" * 60)
        logger.info("FORA Travel Guides Automation - Starting")
        logger.info("=" * 60)
        
        # Validate configuration
        if not self.config.validate_credentials():
            logger.error("Please complete the configuration in fora_config.txt")
            return
        
        # Test connections
        logger.info("\nTesting connections...")
        if not self.fora.authenticate():
            logger.error("FORA authentication failed - check credentials")
            return
        
        if not self.mailchimp.test_connection():
            logger.warning("Mailchimp connection failed - email campaigns will be skipped")
        
        # Fetch travel guides
        logger.info("\nFetching travel guides...")
        guides = self.fora.fetch_travel_guides()
        
        if not guides:
            logger.info("No new guides found")
            return
        
        # Load previous state to avoid republishing
        processed_guides = self._load_state()
        
        # Process each guide
        for guide in guides:
            guide_id = guide.get('url', guide.get('title'))
            
            if guide_id in processed_guides:
                logger.info(f"Skipping already processed: {guide['title']}")
                continue
            
            logger.info(f"\nProcessing: {guide['title']}")
            
            # Download full content
            content = self.fora.download_guide_content(guide['url'])
            
            if not content:
                logger.warning(f"Could not download content for: {guide['title']}")
                continue
            
            # Publish to website
            if self.config.get('AUTO_PUBLISH_TO_WEBSITE', 'True') == 'True':
                if self.publisher.publish_guide(guide, content):
                    processed_guides.append(guide_id)
            
            # Create Mailchimp campaign
            if self.config.get('AUTO_SEND_TO_MAILCHIMP', 'False') == 'True':
                campaign_id = self.mailchimp.create_campaign(guide, content['content'])
                
                if campaign_id:
                    logger.info(f"Campaign created: {campaign_id} (not sent - review in Mailchimp)")
        
        # Save state
        self._save_state(processed_guides)
        
        logger.info("\n" + "=" * 60)
        logger.info("Automation complete!")
        logger.info("=" * 60)
    
    def _load_state(self) -> List[str]:
        """Load previously processed guides"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                return state.get('processed_guides', [])
        return []
    
    def _save_state(self, processed_guides: List[str]):
        """Save processed guides state"""
        state = {
            'processed_guides': processed_guides,
            'last_run': datetime.now().isoformat()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)


if __name__ == '__main__':
    try:
        automation = AutomationManager()
        automation.run()
    except KeyboardInterrupt:
        logger.info("\nAutomation interrupted by user")
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}", exc_info=True)
