"""
FORA Travel Guides Section Generator
Creates a "Travel Guides" section HTML snippet to add to existing resources page
"""

import os
import csv
from datetime import datetime
from typing import Dict, List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FORASectionGenerator:
    """Generates FORA guides section HTML"""
    
    def __init__(self, csv_file='fora_guides.csv'):
        self.csv_file = csv_file
        self.guides = []
    
    def load_guides(self) -> List[Dict]:
        """Load guides from CSV"""
        if not os.path.exists(self.csv_file):
            logger.error(f"CSV file not found: {self.csv_file}")
            return []
        
        guides = []
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                # Skip first line if it's not the header
                first_line = f.readline()
                if 'Date' not in first_line and 'Name' not in first_line:
                    # Not header, read from position
                    f.seek(0)
                    f.readline()  # Skip line 1
                else:
                    f.seek(0)  # Reset to beginning
                
                reader = csv.DictReader(f)
                
                for row in reader:
                    if not row.get('Name'):
                        continue
                    
                    guide = {
                        'name': row.get('Name', '').strip(),
                        'continent': row.get('Continent', 'Other').strip(),
                        'description': row.get('Short Description', '').strip()
                    }
                    
                    guides.append(guide)
            
            self.guides = guides
            logger.info(f"Loaded {len(guides)} FORA destination guides")
            return guides
            
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return []
    
    def generate_section_html(self) -> str:
        """Generate the Travel Guides section HTML"""
        
        if not self.guides:
            self.load_guides()
        
        # Group by continent
        by_continent = {}
        for guide in self.guides:
            continent = guide['continent']
            if continent not in by_continent:
                by_continent[continent] = []
            by_continent[continent].append(guide)
        
        # Sort continents
        sorted_continents = sorted(by_continent.keys())
        
        # Build HTML
        html = f"""
<!-- FORA Travel Guides Section - Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} -->
<section style="margin: 3rem 0; padding: 2rem; background: #f8f9fa; border-radius: 8px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2 style="margin: 0;">Travel Guides</h2>
        <a href="https://docs.google.com/spreadsheets/d/1ub19wcmOEBmD82Gr05Qw_0Zmn5klXtxxy6ZOBxhyqmQ/edit" 
           target="_blank" 
           rel="noopener noreferrer"
           style="font-size: 0.9rem; color: #2c7a7b; text-decoration: none; padding: 0.5rem 1rem; background: white; border-radius: 4px; border: 1px solid #e2e8f0;">
            📊 Update Database
        </a>
    </div>
    <p style="color: #666; font-size: 0.95rem; margin-bottom: 1.5rem;">
        Explore {len(self.guides)} expertly curated destination guides powered by FORA Travel. 
        <strong>Contact me for exclusive access to detailed travel guides.</strong>
    </p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
"""
        
        # Add continent filters/summary
        for continent in sorted_continents:
            count = len(by_continent[continent])
            html += f"""        <div style="padding: 1rem; background: white; border-radius: 6px; text-align: center; border: 2px solid #e2e8f0;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #2d3748;">{count}</div>
            <div style="font-size: 0.9rem; color: #718096;">{continent}</div>
        </div>
"""
        
        html += """    </div>
    
    <div style="background: white; padding: 1.5rem; border-radius: 6px; border: 1px solid #e2e8f0;">
        <p style="color: #4a5568; margin-bottom: 1rem;">
            <strong>📍 Browse by Destination:</strong> Select a continent to view guides
        </p>
        <select id="continentFilter" style="width: 100%; padding: 0.75rem; border: 1px solid #cbd5e0; border-radius: 4px; font-size: 1rem; margin-bottom: 1rem;">
            <option value="all">All Continents ({len(self.guides)} guides)</option>
"""
        
        for continent in sorted_continents:
            count = len(by_continent[continent])
            html += f"""            <option value="{continent}">{continent} ({count} guides)</option>
"""
        
        html += """        </select>
        
        <div id="guidesList" style="max-height: 400px; overflow-y: auto; padding: 1rem;">
"""
        
        # Add guides by continent
        for continent in sorted_continents:
            html += f"""            <div class="continent-group" data-continent="{continent}">
                <h3 style="color: #2d3748; font-size: 1.1rem; margin: 1rem 0 0.5rem 0; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
                    {continent}
                </h3>
                <ul style="columns: 2; column-gap: 2rem; list-style: none; padding: 0;">
"""
            
            for guide in sorted(by_continent[continent], key=lambda x: x['name']):
                html += f"""                    <li style="padding: 0.25rem 0; break-inside: avoid;">
                        <span style="color: #4a5568; font-size: 0.95rem;" title="{guide['description']}">{guide['name']}</span>
                    </li>
"""
            
            html += """                </ul>
            </div>
"""
        
        html += """        </div>
    </div>
    
    <div style="margin-top: 1.5rem; padding: 1rem; background: white; border-radius: 6px; border-left: 4px solid #2c7a7b;">
        <p style="color: #4a5568; margin: 0;">
            <strong>Need a specific guide?</strong> These curated destination resources are available exclusively through consultation. 
            <a href="contact.html" style="color: #2c7a7b; text-decoration: underline;">Contact me</a> to access detailed travel guides and personalized recommendations.
        </p>
    </div>
</section>

<script>
// Filter functionality
document.getElementById('continentFilter').addEventListener('change', function(e) {
    const selected = e.target.value;
    const groups = document.querySelectorAll('.continent-group');
    
    groups.forEach(group => {
        if (selected === 'all' || group.dataset.continent === selected) {
            group.style.display = 'block';
        } else {
            group.style.display = 'none';
        }
    });
});
</script>
<!-- End FORA Travel Guides Section -->
"""
        
        return html
    
    def save_section(self, output_file='fora_section.html'):
        """Save the section HTML to a file"""
        html = self.generate_section_html()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"Section HTML saved to: {output_file}")
        logger.info("Copy this HTML and paste it into your resources.html file")
        return True


def main():
    logger.info("=" * 70)
    logger.info("FORA Travel Guides Section Generator")
    logger.info("=" * 70)
    logger.info("")
    
    generator = FORASectionGenerator()
    guides = generator.load_guides()
    
    if not guides:
        logger.error("No guides loaded. Cannot generate section.")
        return
    
    logger.info(f"\nLoaded {len(guides)} guides")
    
    if generator.save_section():
        logger.info("\n" + "=" * 70)
        logger.info("Section generated successfully!")
        logger.info("Next steps:")
        logger.info("1. Open fora_section.html")
        logger.info("2. Copy the HTML")
        logger.info("3. Paste it into your resources.html file (after the nav, before 'Guides' section)")
        logger.info("=" * 70)


if __name__ == '__main__':
    main()
