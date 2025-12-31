"""
Mailchimp + FORA Integration
Automate email campaigns with FORA travel guides
"""

import os
import json
import requests
from datetime import datetime


class MailchimpFORAIntegration:
    """Integrate Mailchimp campaigns with FORA guides"""
    
    def __init__(self, config_file='mailchimp_config.txt'):
        self.config = self._load_config(config_file)
        self.api_key = self.config.get('MAILCHIMP_API_KEY')
        self.server = self.config.get('MAILCHIMP_SERVER', 'us1')
        self.base_url = f"https://{self.server}.api.mailchimp.com/3.0"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def _load_config(self, config_file):
        """Load Mailchimp configuration"""
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        return config
    
    def test_connection(self):
        """Test Mailchimp API connection"""
        try:
            response = requests.get(
                f"{self.base_url}/ping",
                headers=self.headers
            )
            if response.status_code == 200:
                print("✓ Connected to Mailchimp successfully!")
                return True
            else:
                print(f"✗ Connection failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def get_audiences(self):
        """Get all Mailchimp audiences/lists"""
        try:
            response = requests.get(
                f"{self.base_url}/lists",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                audiences = data.get('lists', [])
                
                print(f"\nFound {len(audiences)} audience(s):")
                for audience in audiences:
                    print(f"  - {audience['name']} (ID: {audience['id']})")
                    print(f"    Members: {audience['stats']['member_count']}")
                
                return audiences
            else:
                print(f"Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def create_campaign_with_guides(self, subject, audience_id, guide_list=None):
        """Create email campaign featuring FORA guides"""
        
        # Load FORA guides if not provided
        if guide_list is None:
            if os.path.exists('fora_guides_catalog.json'):
                with open('fora_guides_catalog.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    guide_list = data.get('guides', [])[:10]  # Top 10 guides
        
        # Build email HTML
        email_html = self._build_email_html(guide_list)
        
        # Create campaign
        campaign_data = {
            "type": "regular",
            "recipients": {
                "list_id": audience_id
            },
            "settings": {
                "subject_line": subject,
                "from_name": "Gregory Rhoney - SEAL Enterprises",
                "reply_to": self.config.get('MAILCHIMP_USERNAME'),
                "title": f"FORA Guides - {datetime.now().strftime('%Y-%m-%d')}"
            }
        }
        
        try:
            # Create campaign
            response = requests.post(
                f"{self.base_url}/campaigns",
                headers=self.headers,
                json=campaign_data
            )
            
            if response.status_code == 200:
                campaign = response.json()
                campaign_id = campaign['id']
                print(f"✓ Campaign created: {campaign_id}")
                
                # Set content
                content_response = requests.put(
                    f"{self.base_url}/campaigns/{campaign_id}/content",
                    headers=self.headers,
                    json={"html": email_html}
                )
                
                if content_response.status_code == 200:
                    print(f"✓ Content added to campaign")
                    print(f"\nCampaign URL: https://{self.server}.admin.mailchimp.com/campaigns/edit?id={campaign['web_id']}")
                    return campaign
                else:
                    print(f"✗ Error setting content: {content_response.status_code}")
                    
            else:
                print(f"✗ Error creating campaign: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"✗ Error: {e}")
        
        return None
    
    def _build_email_html(self, guides):
        """Build HTML for email campaign"""
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #0b6fa4 0%, #2c7a7b 100%); color: white; padding: 30px; text-align: center; }
                .guide-card { border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin: 15px 0; background: #f8f9fa; }
                .guide-card h3 { color: #0b6fa4; margin: 0 0 10px 0; }
                .cta-button { display: inline-block; padding: 12px 24px; background: #0b6fa4; color: white; text-decoration: none; border-radius: 4px; margin: 5px 5px 5px 0; }
                .email-button { display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 4px; margin: 5px 5px 5px 0; }
                .footer { text-align: center; padding: 20px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Your Curated Travel Guides</h1>
                    <p>Expertly selected destinations just for you</p>
                </div>
                
                <div style="padding: 20px;">
                    <p>Hi there!</p>
                    <p>I've curated these amazing destination guides for your next adventure. Each guide is personalized with insider tips, recommendations, and everything you need to plan the perfect trip.</p>
                    <p><strong>Want a guide?</strong> Just hit the "Email Me" button below and I'll send you the branded PDF directly!</p>
        """
        
        # Add guide cards
        for guide in guides[:10]:  # Limit to 10
            guide_name = guide.get('name', 'Destination')
            # Create safe filename
            safe_name = guide_name.lower().replace(' ', '-').replace(':', '').replace(',', '')
            email_subject = f"Request: {guide_name} Travel Guide"
            email_body = f"Hi Gregory,\n\nI'd love to receive the '{guide_name}' travel guide.\n\nThanks!"
            
            html += f"""
                    <div class="guide-card">
                        <h3>🌍 {guide_name}</h3>
                        <p><strong>📍 Location:</strong> {guide.get('continent', 'Various')}</p>
                        <p>{guide.get('description', 'Explore this amazing destination')}</p>
                        <div style="margin-top: 15px;">
                            <a href="mailto:gregory.rhoney@fora.travel?subject={email_subject.replace(' ', '%20')}&body={email_body.replace(' ', '%20').replace('\n', '%0D%0A')}" class="email-button">📧 Email Me for This Guide</a>
                        </div>
                    </div>
            """
        
        html += """
                    <div style="text-align: center; margin: 30px 0; padding: 20px; background: #f0f7ff; border-radius: 8px;">
                        <h3>Ready to Start Planning?</h3>
                        <p>Let's create your perfect travel experience together.</p>
                        <a href="mailto:gregory.rhoney@fora.travel?subject=Travel Planning Consultation&body=Hi Gregory,%0D%0A%0D%0AI'd like to schedule a consultation to discuss my travel plans.%0D%0A%0D%0AThanks!" class="cta-button">📅 Schedule a Consultation</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>Gregory Rhoney</strong><br>
                    SEAL Enterprises Travel Planning<br>
                    📧 <a href="mailto:gregory.rhoney@fora.travel" style="color: #0b6fa4;">gregory.rhoney@fora.travel</a><br>
                    🌐 <a href="https://sealenterprises.net" style="color: #0b6fa4;">www.sealenterprises.net</a></p>
                    <p style="font-size: 12px; color: #999;">Destination guides powered by FORA Travel</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html


def main():
    print("=" * 70)
    print("Mailchimp + FORA Integration Setup")
    print("=" * 70)
    print()
    
    # Check for API key
    if not os.path.exists('mailchimp_config.txt'):
        print("⚠ mailchimp_config.txt not found!")
        print("\nPlease create it first with your Mailchimp credentials.")
        return
    
    mc = MailchimpFORAIntegration()
    
    if not mc.api_key or mc.api_key == 'your-api-key-here':
        print("⚠ Mailchimp API key not configured!")
        print("\nTo get your API key:")
        print("1. Log into Mailchimp")
        print("2. Go to: Account → Extras → API keys")
        print("3. Click 'Create A Key'")
        print("4. Copy the key and add it to mailchimp_config.txt")
        print("\nExample: MAILCHIMP_API_KEY=abc123def456-us1")
        return
    
    print("Testing connection...")
    if mc.test_connection():
        print("\n✓ Connection successful!")
        print("\nFetching your audiences...")
        mc.get_audiences()
        
        print("\n" + "=" * 70)
        print("Setup complete! You can now:")
        print("1. Create campaigns with FORA guides")
        print("2. Automate guide delivery to subscribers")
        print("3. Track engagement and conversions")
        print("=" * 70)


if __name__ == '__main__':
    main()
