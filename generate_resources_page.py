"""
FORA Travel Resources Page Generator
Creates a resources directory page with links to FORA magic content
100% copyright compliant - just links to FORA's content with your advisor ID
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fora_resources_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ResourcesPageGenerator:
    """Generates a resources page from FORA guide catalog"""
    
    def __init__(self, csv_file='fora_guides.csv', advisor_id='gregory-rhoney'):
        self.csv_file = csv_file
        self.advisor_id = advisor_id
        self.guides = []
    
    def load_guides(self) -> List[Dict]:
        """Load guides from CSV"""
        if not os.path.exists(self.csv_file):
            logger.error(f"CSV file not found: {self.csv_file}")
            logger.info("Please export your FORA Google Sheet as CSV and save as 'fora_guides.csv'")
            return []
        
        guides = []
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                # Skip first line if it's not the header
                first_line = f.readline()
                # Check if first line looks like a header (contains "Date" or "Name")
                if 'Date' not in first_line and 'Name' not in first_line:
                    # First line is not header, continue reading from line 2
                    pass
                else:
                    # First line IS the header, reset to beginning
                    f.seek(0)
                
                reader = csv.DictReader(f)
                
                for row in reader:
                    magic_content = row.get('Magic Content', '').strip()
                    if not magic_content:
                        continue
                    
                    # Personalize URL
                    magic_url = self._personalize_url(magic_content)
                    
                    guide = {
                        'name': row.get('Name', '').strip(),
                        'description': row.get('Description', '').strip(),
                        'continent': row.get('Continent', '').strip(),
                        'country': row.get('Country', '').strip(),
                        'region': row.get('Region', '').strip(),
                        'style': row.get('Style', '').strip(),
                        'season': row.get('Season', '').strip(),
                        'partner': row.get('Partner', '').strip(),
                        'budget_friendly': row.get('< $500 option(s)', '').lower() in ['yes', 'true', 'x'],
                        'magic_url': magic_url,
                        'date': row.get('Date', '').strip()
                    }
                    
                    guides.append(guide)
            
            self.guides = guides
            logger.info(f"✓ Loaded {len(guides)} travel guides from CSV")
            return guides
            
        except Exception as e:
            logger.error(f"Error reading CSV: {str(e)}")
            return []
    
    def _personalize_url(self, url: str) -> str:
        """Add advisor ID to URL if needed"""
        if not url or not url.startswith('http'):
            return url
        
        if self.advisor_id in url:
            return url
        
        # Insert advisor path
        if '/advisor/' not in url:
            parts = url.split('/')
            if len(parts) >= 4:
                base = '/'.join(parts[:3])
                path = '/'.join(parts[3:])
                return f"{base}/advisor/{self.advisor_id}/{path}"
        
        return url
    
    def generate_resources_page(self, output_file='resources.html'):
        """Generate the resources page HTML"""
        if not self.guides:
            logger.error("No guides loaded. Cannot generate page.")
            return False
        
        try:
            # Group guides by continent
            by_continent = {}
            for guide in self.guides:
                continent = guide['continent'] or 'Other'
                if continent not in by_continent:
                    by_continent[continent] = []
                by_continent[continent].append(guide)
            
            # Sort each continent's guides
            for continent in by_continent:
                by_continent[continent].sort(key=lambda x: x['name'])
            
            # Generate HTML
            html = self._create_html(by_continent)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            logger.info(f"✓ Resources page created: {output_file}")
            
            # Also create JSON catalog
            self._create_json_catalog()
            
            return True
            
        except Exception as e:
            logger.error(f"Error generating page: {str(e)}")
            return False
    
    def _create_html(self, by_continent: Dict) -> str:
        """Create the complete HTML page"""
        
        # Count stats
        total_guides = len(self.guides)
        countries = len(set(g['country'] for g in self.guides if g['country']))
        budget_friendly = len([g for g in self.guides if g['budget_friendly']])
        
        # Build continent sections
        sections_html = ''
        for continent in sorted(by_continent.keys()):
            guides = by_continent[continent]
            sections_html += self._create_continent_section(continent, guides)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Exclusive travel guides and destination resources curated by SEAL Enterprises">
    <title>Travel Resources & Destination Guides - SEAL Enterprises</title>
    <link rel="stylesheet" href="css/styles.css">
    <style>
        .resources-hero {{
            background: linear-gradient(135deg, #0b6fa4 0%, #094d73 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }}
        .resources-hero h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .resources-hero p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin-top: 2rem;
            flex-wrap: wrap;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            display: block;
        }}
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        .filter-bar {{
            background: #f8f9fa;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 8px;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }}
        .filter-bar input {{
            flex: 1;
            min-width: 250px;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }}
        .filter-bar select {{
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }}
        .continent-section {{
            margin: 3rem 0;
        }}
        .continent-header {{
            color: #0b6fa4;
            font-size: 2rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #0b6fa4;
        }}
        .guides-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .guide-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
        }}
        .guide-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        .guide-card h3 {{
            color: #0b6fa4;
            margin-bottom: 0.75rem;
            font-size: 1.3rem;
        }}
        .guide-meta {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
            font-size: 0.85rem;
            color: #666;
        }}
        .guide-tag {{
            background: #e9ecef;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
        }}
        .budget-tag {{
            background: #d4edda;
            color: #155724;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-weight: 600;
        }}
        .guide-description {{
            color: #555;
            margin-bottom: 1rem;
            flex: 1;
            line-height: 1.6;
        }}
        .guide-link {{
            display: inline-block;
            background: #0b6fa4;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 600;
            text-align: center;
            transition: background 0.2s;
        }}
        .guide-link:hover {{
            background: #094d73;
        }}
        .cta-section {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 3rem;
            border-radius: 8px;
            text-align: center;
            margin: 3rem 0;
        }}
        .cta-section h2 {{
            color: #0b6fa4;
            margin-bottom: 1rem;
        }}
        @media (max-width: 768px) {{
            .resources-hero h1 {{
                font-size: 1.8rem;
            }}
            .guides-grid {{
                grid-template-columns: 1fr;
            }}
            .stats {{
                gap: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <nav class="navbar" style="background: #0b6fa4; padding: 1rem 0; color: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; display: flex; justify-content: space-between; align-items: center;">
            <a href="index.html" style="color: white; text-decoration: none; font-weight: 700; font-size: 1.2rem;">SEAL Enterprises</a>
            <div style="display: flex; gap: 2rem;">
                <a href="index.html" style="color: white; text-decoration: none;">Home</a>
                <a href="about.html" style="color: white; text-decoration: none;">About</a>
                <a href="contact.html" style="color: white; text-decoration: none;">Contact</a>
            </div>
        </div>
    </nav>
    
    <header class="resources-hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <img src="icons/Fora_Logo_Wordmark_White.png" alt="FORA Travel" height="40" style="opacity: 0.9;" onerror="this.style.display='none'">
                <a href="https://docs.google.com/spreadsheets/d/1ub19wcmOEBmD82Gr05Qw_0Zmn5klXtxxy6ZOBxhyqmQ/edit" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 0.5rem 1.25rem; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 4px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.3); transition: all 0.3s;">
                    📊 Update Resource Database
                </a>
            </div>
            <h1>Travel Resources & Destination Guides</h1>
            <p>Expertly curated destination guides powered by FORA Travel</p>
            <p style="font-size: 0.95rem; opacity: 0.85; margin-top: 0.5rem;">Content provided by FORA Travel • Curated by Gregory Rhoney</p>
            
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">{total_guides}</span>
                    <span class="stat-label">Destinations</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{countries}</span>
                    <span class="stat-label">Countries</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{budget_friendly}</span>
                    <span class="stat-label">Budget-Friendly Options</span>
                </div>
            </div>
        </div>
    </header>
    
    <main class="container" style="max-width: 1200px; margin: 0 auto; padding: 2rem 1rem;">
        <div class="filter-bar">
            <input type="text" id="searchInput" placeholder="🔍 Search destinations, countries, or styles...">
            <select id="continentFilter">
                <option value="">All Continents</option>
                {self._create_continent_options(by_continent)}
            </select>
            <select id="styleFilter">
                <option value="">All Styles</option>
                {self._create_style_options()}
            </select>
        </div>
        
        <div id="guidesContainer">
            {sections_html}
        </div>
        
        <div class="cta-section">
            <h2>Ready to Plan Your Next Adventure?</h2>
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
                Let me help you create unforgettable experiences with exclusive rates and VIP perks.
            </p>
            <a href="contact.html" class="guide-link" style="display: inline-block; font-size: 1.1rem; padding: 1rem 2rem;">
                Contact Gregory Rhoney
            </a>
        </div>
    </main>
    
    <footer style="margin-top: 3rem; padding: 2rem 0; background: #f8f9fa; text-align: center;">
        <div class="container">
            <a href="https://www.foratravel.com/advisor/gregory-rhoney" target="_blank" rel="noopener noreferrer">
                <img src="icons/Fora_Logo_Wordmark_Black-Sand_S.png" alt="Powered by FORA Travel" height="50" loading="lazy">
            </a>
            <p style="margin-top: 1rem; font-size: 0.9rem;">
                Proudly Powered by <a href="https://www.foratravel.com/advisor/gregory-rhoney" target="_blank" rel="noopener noreferrer" style="color: #0b6fa4; text-decoration: underline;">FORA Travel</a>
            </p>
        </div>
    </footer>
    
    <script>
        // Search and filter functionality
        const searchInput = document.getElementById('searchInput');
        const continentFilter = document.getElementById('continentFilter');
        const styleFilter = document.getElementById('styleFilter');
        const allCards = document.querySelectorAll('.guide-card');
        const allSections = document.querySelectorAll('.continent-section');
        
        function filterGuides() {{
            const searchTerm = searchInput.value.toLowerCase();
            const continent = continentFilter.value.toLowerCase();
            const style = styleFilter.value.toLowerCase();
            
            allCards.forEach(card => {{
                const name = card.dataset.name.toLowerCase();
                const cardContinent = card.dataset.continent.toLowerCase();
                const cardStyle = card.dataset.style.toLowerCase();
                const country = card.dataset.country.toLowerCase();
                
                const matchesSearch = !searchTerm || name.includes(searchTerm) || country.includes(searchTerm) || cardStyle.includes(searchTerm);
                const matchesContinent = !continent || cardContinent === continent;
                const matchesStyle = !style || cardStyle.includes(style);
                
                if (matchesSearch && matchesContinent && matchesStyle) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // Hide empty sections
            allSections.forEach(section => {{
                const visibleCards = section.querySelectorAll('.guide-card[style*="display: flex"]').length;
                section.style.display = visibleCards > 0 ? 'block' : 'none';
            }});
        }}
        
        searchInput.addEventListener('input', filterGuides);
        continentFilter.addEventListener('change', filterGuides);
        styleFilter.addEventListener('change', filterGuides);
    </script>
</body>
</html>"""
        return html
    
    def _create_continent_section(self, continent: str, guides: List[Dict]) -> str:
        """Create HTML for a continent section"""
        cards_html = '\n'.join([self._create_guide_card(g) for g in guides])
        
        return f"""
        <section class="continent-section" data-continent="{continent.lower()}">
            <h2 class="continent-header">🌍 {continent}</h2>
            <div class="guides-grid">
                {cards_html}
            </div>
        </section>
        """
    
    def _create_guide_card(self, guide: Dict) -> str:
        """Create HTML for a single guide card"""
        location = ', '.join(filter(None, [guide['region'], guide['country']]))
        
        tags = []
        if guide['style']:
            tags.append(f'<span class="guide-tag">{guide["style"]}</span>')
        if guide['season']:
            tags.append(f'<span class="guide-tag">{guide["season"]}</span>')
        if guide['partner']:
            tags.append(f'<span class="guide-tag">{guide["partner"]}</span>')
        
        budget_tag = ''
        if guide['budget_friendly']:
            budget_tag = '<span class="budget-tag">💰 Budget-Friendly</span>'
        
        tags_html = ' '.join(tags) if tags else ''
        
        return f"""
        <div class="guide-card" 
             data-name="{guide['name']}" 
             data-continent="{guide['continent'].lower()}" 
             data-country="{guide['country'].lower()}"
             data-style="{guide['style'].lower()}">
            <h3>{guide['name']}</h3>
            {f'<p style="color: #666; font-size: 0.9rem; margin-bottom: 0.75rem;">📍 {location}</p>' if location else ''}
            <div class="guide-meta">
                {tags_html}
                {budget_tag}
            </div>
            {f'<p class="guide-description">{guide["description"]}</p>' if guide['description'] else ''}
            {f'<a href="{guide["magic_url"]}" target="_blank" rel="noopener noreferrer" class="guide-link">View Travel Guide →</a>' if guide['magic_url'] and guide['magic_url'].startswith('http') else '<p style="color: #999; font-size: 0.9rem; font-style: italic;">Contact me for detailed information about this destination</p>'}
            <a href="contact.html" class="guide-link" style="background: #28a745; margin-top: 0.5rem;">
                Request Information
            </a>
        </div>
        """
    
    def _create_continent_options(self, by_continent: Dict) -> str:
        """Create continent filter options"""
        options = []
        for continent in sorted(by_continent.keys()):
            count = len(by_continent[continent])
            options.append(f'<option value="{continent.lower()}">{continent} ({count})</option>')
        return '\n'.join(options)
    
    def _create_style_options(self) -> str:
        """Create style filter options"""
        styles = set()
        for guide in self.guides:
            if guide['style']:
                # Split multiple styles if comma-separated
                for style in guide['style'].split(','):
                    styles.add(style.strip())
        
        options = []
        for style in sorted(styles):
            options.append(f'<option value="{style.lower()}">{style}</option>')
        return '\n'.join(options)
    
    def _create_json_catalog(self):
        """Create JSON catalog for programmatic access"""
        catalog = {
            'total_guides': len(self.guides),
            'last_updated': datetime.now().isoformat(),
            'advisor': 'Gregory Rhoney',
            'advisor_id': self.advisor_id,
            'guides': self.guides
        }
        
        with open('fora_guides_catalog.json', 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2)
        
        logger.info("✓ JSON catalog created: fora_guides_catalog.json")


def main():
    logger.info("=" * 70)
    logger.info("FORA Travel Resources Page Generator")
    logger.info("=" * 70)
    
    generator = ResourcesPageGenerator()
    
    logger.info("\nLoading guides from CSV...")
    guides = generator.load_guides()
    
    if not guides:
        logger.error("No guides found. Please export your FORA Google Sheet as CSV.")
        return
    
    logger.info(f"\n✓ Loaded {len(guides)} guides")
    logger.info(f"   Continents: {len(set(g['continent'] for g in guides if g['continent']))}")
    logger.info(f"   Countries: {len(set(g['country'] for g in guides if g['country']))}")
    
    logger.info("\nGenerating resources page...")
    if generator.generate_resources_page():
        logger.info("\n" + "=" * 70)
        logger.info("✅ Resources page generated successfully!")
        logger.info("   File: resources.html")
        logger.info("   Catalog: fora_guides_catalog.json")
        logger.info("=" * 70)
        logger.info("\n📄 Open resources.html in your browser to preview!")
    else:
        logger.error("Failed to generate resources page")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nGeneration interrupted by user")
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}", exc_info=True)
