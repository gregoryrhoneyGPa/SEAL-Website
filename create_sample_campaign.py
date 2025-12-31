"""
Create Sample Mailchimp Campaign with FORA Guides
"""

from mailchimp_fora_integration import MailchimpFORAIntegration
import json
import os


def main():
    print("=" * 70)
    print("Creating GPa's Groundings Campaign")
    print("=" * 70)
    print()
    
    # Ask for edition number
    edition = input("Enter edition number (default 4): ").strip()
    if not edition:
        edition = "4"
    
    # Ask for number of guides
    num_guides = input("Number of guides to feature (default 1): ").strip()
    if not num_guides or not num_guides.isdigit():
        num_guides = 1
    else:
        num_guides = int(num_guides)
    
    # Initialize Mailchimp
    mc = MailchimpFORAIntegration()
    
    # Load FORA guides
    guide_list = []
    if os.path.exists('fora_guides_catalog.json'):
        with open('fora_guides_catalog.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_guides = data.get('guides', [])
            
            # Select diverse guides from different continents
            continents = {}
            for guide in all_guides:
                continent = guide.get('continent', 'Other')
                if continent not in continents:
                    continents[continent] = []
                continents[continent].append(guide)
            
            # Pick guides based on user preference
            if num_guides == 1:
                # Pick first guide from first continent
                for guides in continents.values():
                    if guides:
                        guide_list.append(guides[0])
                        break
            else:
                # Pick multiple guides from different continents
                guides_per_continent = max(1, num_guides // len(continents))
                for continent, guides in continents.items():
                    guide_list.extend(guides[:guides_per_continent])
                    if len(guide_list) >= num_guides:
                        break
                guide_list = guide_list[:num_guides]
    
    print(f"\nSelected {len(guide_list)} featured guide(s):")
    for i, guide in enumerate(guide_list, 1):
        print(f"  {i}. {guide['name']} ({guide['continent']})")
    
    print("\nCreating campaign...")
    
    # Create campaign with numbered subject line
    campaign = mc.create_campaign_with_guides(
        subject=f"GPa's Groundings #{edition}",
        audience_id="97b0498646",  # Your SEAL Enterprises audience
        guide_list=guide_list
    )
    
    if campaign:
        print("\n" + "=" * 70)
        print("✓ Sample campaign created successfully!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Review the campaign in your Mailchimp dashboard")
        print("2. Send a test email to yourself")
        print("3. Make any adjustments")
        print("4. Schedule or send to your audience!")
    else:
        print("\n✗ Failed to create campaign")


if __name__ == '__main__':
    main()
