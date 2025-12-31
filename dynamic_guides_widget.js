/**
 * Dynamic Travel Guides Widget
 * Automatically loads and displays FORA travel guides on your website
 */

class TravelGuidesWidget {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            indexPath: 'travel-guides/index.json',
            maxGuides: options.maxGuides || 6,
            layout: options.layout || 'grid', // 'grid', 'list', 'carousel'
            autoRefresh: options.autoRefresh || false,
            refreshInterval: options.refreshInterval || 300000, // 5 minutes
            ...options
        };
        
        this.guides = [];
        this.init();
    }
    
    async init() {
        if (!this.container) {
            console.error('Travel guides container not found');
            return;
        }
        
        await this.loadGuides();
        this.render();
        
        if (this.options.autoRefresh) {
            setInterval(() => this.loadGuides(), this.options.refreshInterval);
        }
    }
    
    async loadGuides() {
        try {
            const response = await fetch(this.options.indexPath);
            if (!response.ok) {
                throw new Error('Failed to load travel guides');
            }
            
            const data = await response.json();
            this.guides = data.guides || [];
            
            // Sort by published date (newest first)
            this.guides.sort((a, b) => 
                new Date(b.published_date) - new Date(a.published_date)
            );
            
            // Limit to maxGuides
            this.guides = this.guides.slice(0, this.options.maxGuides);
            
            console.log(`Loaded ${this.guides.length} travel guides`);
            
        } catch (error) {
            console.error('Error loading travel guides:', error);
            this.guides = [];
        }
    }
    
    render() {
        if (!this.guides.length) {
            this.container.innerHTML = `
                <div class="no-guides">
                    <p>New travel guides coming soon!</p>
                </div>
            `;
            return;
        }
        
        switch (this.options.layout) {
            case 'list':
                this.renderList();
                break;
            case 'carousel':
                this.renderCarousel();
                break;
            case 'grid':
            default:
                this.renderGrid();
        }
    }
    
    renderGrid() {
        const guidesHTML = this.guides.map(guide => this.createGuideCard(guide)).join('');
        
        this.container.innerHTML = `
            <div class="travel-guides-grid" style="
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 2rem;
            ">
                ${guidesHTML}
            </div>
        `;
    }
    
    renderList() {
        const guidesHTML = this.guides.map(guide => this.createGuideListItem(guide)).join('');
        
        this.container.innerHTML = `
            <div class="travel-guides-list" style="
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
                margin-top: 2rem;
            ">
                ${guidesHTML}
            </div>
        `;
    }
    
    renderCarousel() {
        const guidesHTML = this.guides.map(guide => this.createGuideCard(guide)).join('');
        
        this.container.innerHTML = `
            <div class="travel-guides-carousel">
                <button class="carousel-btn prev" onclick="travelGuidesWidget.prevSlide()">‹</button>
                <div class="carousel-track" style="
                    display: flex;
                    overflow-x: auto;
                    scroll-behavior: smooth;
                    gap: 2rem;
                    padding: 1rem 0;
                ">
                    ${guidesHTML}
                </div>
                <button class="carousel-btn next" onclick="travelGuidesWidget.nextSlide()">›</button>
            </div>
        `;
    }
    
    createGuideCard(guide) {
        const publishedDate = new Date(guide.published_date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        return `
            <div class="guide-card" style="
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 1.5rem;
                transition: transform 0.2s, box-shadow 0.2s;
            " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 4px 16px rgba(0,0,0,0.15)'"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.1)'">
                
                <h3 style="
                    color: #0b6fa4;
                    margin-bottom: 0.5rem;
                    font-size: 1.3rem;
                ">${guide.title}</h3>
                
                <p style="
                    color: #666;
                    font-size: 0.9rem;
                    margin-bottom: 1rem;
                ">${guide.description}</p>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: auto;
                ">
                    <span style="
                        font-size: 0.8rem;
                        color: #999;
                    ">${publishedDate}</span>
                    
                    <a href="travel-guides/${guide.filename}" 
                       class="btn btn-primary"
                       style="
                        background: #0b6fa4;
                        color: white;
                        padding: 0.5rem 1.5rem;
                        border-radius: 4px;
                        text-decoration: none;
                        font-weight: 600;
                        transition: background 0.2s;
                       "
                       onmouseover="this.style.background='#094d73'"
                       onmouseout="this.style.background='#0b6fa4'">
                        Read Guide →
                    </a>
                </div>
                
                <div style="
                    margin-top: 1rem;
                    padding-top: 1rem;
                    border-top: 1px solid #eee;
                    font-size: 0.75rem;
                    color: #999;
                    text-align: center;
                ">
                    Powered by FORA Travel
                </div>
            </div>
        `;
    }
    
    createGuideListItem(guide) {
        const publishedDate = new Date(guide.published_date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        return `
            <div class="guide-list-item" style="
                background: white;
                border-left: 4px solid #0b6fa4;
                padding: 1.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: box-shadow 0.2s;
            " onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'"
               onmouseout="this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">
                
                <div style="display: flex; justify-content: space-between; align-items: start; gap: 2rem;">
                    <div style="flex: 1;">
                        <h3 style="
                            color: #0b6fa4;
                            margin-bottom: 0.5rem;
                            font-size: 1.4rem;
                        ">${guide.title}</h3>
                        
                        <p style="
                            color: #666;
                            margin-bottom: 1rem;
                        ">${guide.description}</p>
                        
                        <div style="
                            display: flex;
                            gap: 1rem;
                            align-items: center;
                        ">
                            <span style="
                                font-size: 0.85rem;
                                color: #999;
                            ">📅 ${publishedDate}</span>
                            
                            <span style="
                                font-size: 0.85rem;
                                color: #999;
                            ">Powered by FORA Travel</span>
                        </div>
                    </div>
                    
                    <a href="travel-guides/${guide.filename}" 
                       class="btn btn-primary"
                       style="
                        background: #0b6fa4;
                        color: white;
                        padding: 0.75rem 2rem;
                        border-radius: 4px;
                        text-decoration: none;
                        font-weight: 600;
                        white-space: nowrap;
                        transition: background 0.2s;
                       "
                       onmouseover="this.style.background='#094d73'"
                       onmouseout="this.style.background='#0b6fa4'">
                        Read Guide →
                    </a>
                </div>
            </div>
        `;
    }
    
    nextSlide() {
        const track = this.container.querySelector('.carousel-track');
        const cardWidth = track.querySelector('.guide-card').offsetWidth + 32; // Include gap
        track.scrollBy({ left: cardWidth, behavior: 'smooth' });
    }
    
    prevSlide() {
        const track = this.container.querySelector('.carousel-track');
        const cardWidth = track.querySelector('.guide-card').offsetWidth + 32;
        track.scrollBy({ left: -cardWidth, behavior: 'smooth' });
    }
}

// Auto-initialize if data-auto-init is present
document.addEventListener('DOMContentLoaded', () => {
    const autoContainers = document.querySelectorAll('[data-travel-guides]');
    
    autoContainers.forEach(container => {
        const options = {
            maxGuides: parseInt(container.dataset.maxGuides) || 6,
            layout: container.dataset.layout || 'grid',
            autoRefresh: container.dataset.autoRefresh === 'true'
        };
        
        new TravelGuidesWidget(container.id, options);
    });
});
