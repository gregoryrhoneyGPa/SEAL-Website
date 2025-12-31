"""
Mailchimp List Sync Tool
Compare website contact form submissions with Mailchimp list and sync subscribers
"""

import requests
import json
import os
from datetime import datetime
from mailchimp_fora_integration import MailchimpFORAIntegration


class MailchimpSync:
    """Sync contact form submissions with Mailchimp"""
    
    def __init__(self):
        self.mc = MailchimpFORAIntegration()
        self.audience_id = "97b0498646"  # Your SEAL Enterprises audience
    
    def get_mailchimp_subscribers(self):
        """Get all subscribers from Mailchimp"""
        try:
            response = requests.get(
                f"{self.mc.base_url}/lists/{self.audience_id}/members",
                headers=self.mc.headers,
                params={"count": 1000}  # Get up to 1000 subscribers
            )
            
            if response.status_code == 200:
                data = response.json()
                members = data.get('members', [])
                
                subscribers = {}
                for member in members:
                    email = member['email_address'].lower()
                    subscribers[email] = {
                        'email': email,
                        'name': f"{member.get('merge_fields', {}).get('FNAME', '')} {member.get('merge_fields', {}).get('LNAME', '')}".strip(),
                        'status': member['status'],
                        'subscribed_date': member.get('timestamp_opt', 'Unknown'),
                        'source': 'mailchimp'
                    }
                
                print(f"✓ Found {len(subscribers)} subscribers in Mailchimp")
                return subscribers
            else:
                print(f"✗ Error fetching subscribers: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return {}
    
    def load_contact_submissions(self, csv_file='contact_submissions.csv'):
        """Load contact form submissions from CSV"""
        submissions = {}
        
        if not os.path.exists(csv_file):
            print(f"⚠ No contact submissions file found: {csv_file}")
            print("  Create this file from your Google Sheets contact form responses")
            return submissions
        
        try:
            import csv
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    email = row.get('email', '').strip().lower()
                    subscribe = row.get('subscribe-newsletter', '').lower()
                    
                    if email and subscribe == 'yes':
                        submissions[email] = {
                            'email': email,
                            'name': row.get('name', '').strip(),
                            'phone': row.get('phone', '').strip(),
                            'subscribed_date': row.get('timestamp', datetime.now().isoformat()),
                            'source': 'website'
                        }
            
            print(f"✓ Found {len(submissions)} opt-ins from contact form")
            return submissions
            
        except Exception as e:
            print(f"✗ Error loading submissions: {e}")
            return {}
    
    def add_subscriber_to_mailchimp(self, email, name="", phone=""):
        """Add a new subscriber to Mailchimp"""
        # Parse name into first/last
        name_parts = name.split(' ', 1) if name else ['', '']
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        subscriber_data = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
                "LNAME": last_name
            },
            "tags": ["Website Contact Form"]
        }
        
        if phone:
            subscriber_data["merge_fields"]["PHONE"] = phone
        
        try:
            response = requests.post(
                f"{self.mc.base_url}/lists/{self.audience_id}/members",
                headers=self.mc.headers,
                json=subscriber_data
            )
            
            if response.status_code == 200:
                print(f"  ✓ Added: {email} ({name})")
                return True
            elif response.status_code == 400 and 'already' in response.text.lower():
                print(f"  ℹ Already exists: {email}")
                return True
            else:
                print(f"  ✗ Failed to add {email}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error adding {email}: {e}")
            return False
    
    def sync_lists(self):
        """Compare and sync lists"""
        print("=" * 70)
        print("Mailchimp List Sync")
        print("=" * 70)
        print()
        
        # Get both lists
        mailchimp_subs = self.get_mailchimp_subscribers()
        website_subs = self.load_contact_submissions()
        
        if not website_subs:
            print("\n⚠ No website submissions found. Nothing to sync.")
            return
        
        print("\n" + "-" * 70)
        print("Analysis:")
        print("-" * 70)
        
        # Find new subscribers to add
        new_subscribers = []
        for email, data in website_subs.items():
            if email not in mailchimp_subs:
                new_subscribers.append(data)
        
        print(f"\n📊 Statistics:")
        print(f"  - Mailchimp subscribers: {len(mailchimp_subs)}")
        print(f"  - Website opt-ins: {len(website_subs)}")
        print(f"  - New to add: {len(new_subscribers)}")
        
        if new_subscribers:
            print(f"\n📝 New subscribers to add to Mailchimp:")
            for sub in new_subscribers:
                print(f"  • {sub['email']} - {sub['name']}")
            
            proceed = input(f"\nAdd {len(new_subscribers)} new subscriber(s) to Mailchimp? (y/n): ").strip().lower()
            
            if proceed in ['y', 'yes']:
                print("\nAdding subscribers...")
                success_count = 0
                for sub in new_subscribers:
                    if self.add_subscriber_to_mailchimp(
                        sub['email'],
                        sub['name'],
                        sub.get('phone', '')
                    ):
                        success_count += 1
                
                print(f"\n✓ Successfully added {success_count}/{len(new_subscribers)} subscribers")
            else:
                print("\n✗ Sync cancelled")
        else:
            print("\n✓ All website opt-ins are already in Mailchimp!")
        
        print("\n" + "=" * 70)


def main():
    print("Make sure you have:")
    print("1. Exported contact form responses from Google Sheets as 'contact_submissions.csv'")
    print("2. The CSV should have columns: email, name, phone, subscribe-newsletter, timestamp")
    print()
    
    proceed = input("Ready to sync? (y/n): ").strip().lower()
    
    if proceed in ['y', 'yes']:
        sync = MailchimpSync()
        sync.sync_lists()
    else:
        print("Sync cancelled")


if __name__ == '__main__':
    main()
