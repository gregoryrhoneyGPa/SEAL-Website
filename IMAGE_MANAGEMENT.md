# Image Management Guide

## Folder Structure

```
/images/
  /cruise-lines/          # Official cruise line media
    /carnival/
    /royal-caribbean/
    /norwegian/
    /celebrity/
    /princess/
  /destinations/          # Destination photos
  /amenities/            # Ship amenities
  /groups/               # Group travel scenes
  /unsplash/             # Unsplash stock photos
  image-credits.json     # Credit tracking
```

## Adding Credits to Images

### Option 1: HTML Overlay (Recommended)
**Best for web - clean, SEO-friendly, no image editing needed**

```html
<div class="hero-image-container">
  <img src="images/cruise-lines/royal-caribbean/hero.jpg" 
       alt="Luxury cruise ship at sunset">
  <span class="image-credit">
    Photo: <a href="https://www.royalcaribbean.com">Royal Caribbean</a>
  </span>
</div>
```

### Option 2: Canva/PowerPoint (Quick & Easy)
**Good for social media, presentations, or if you want credit burned into image**

**Canva Steps:**
1. Upload your image
2. Add text element
3. Use small, semi-transparent background
4. Position in corner: "Photo: [Photographer Name]"
5. Download as JPG/PNG
6. Move to: `images/unsplash/`

**PowerPoint Steps:**
1. Insert image
2. Add text box with credit
3. Format text (white text, dark semi-transparent shape behind)
4. Right-click image → Save as Picture
5. Move to appropriate folder

### Option 3: Batch Processing (Many Images)
Use PowerShell script (I can create this if needed) to add metadata

## Credit Requirements

### Unsplash Images
- **Required**: Photographer credit
- **Format**: "Photo by [Name] on Unsplash"
- **Link**: Link to photographer's Unsplash profile
- **Location**: Can be in alt text, caption, or footer

Example:
```html
<img src="images/unsplash/family-cruise.jpg" 
     alt="Family enjoying cruise - Photo by John Doe on Unsplash">
```

### Cruise Line Media
- **Required**: Cruise line attribution if not embedded
- **Format**: "Courtesy of [Cruise Line Name]" or their logo
- **Location**: Image overlay or page footer
- **Important**: Keep embedded logos visible and unobstructed

Example:
```html
<span class="image-credit">Courtesy of Royal Caribbean International</span>
```

## Image Optimization Workflow

1. **Get Image** → Download from cruise line portal or Unsplash
2. **Organize** → Place in appropriate folder
3. **Optimize** → Compress to ~100-200KB (use tinypng.com or I can create script)
4. **Credit** → Update `image-credits.json`
5. **Implement** → Add to HTML with proper alt text and credit

## File Naming Convention

Use descriptive, SEO-friendly names:
- ✅ `royal-caribbean-family-pool-deck.jpg`
- ✅ `caribbean-sunset-destination.jpg`
- ❌ `IMG_1234.jpg`
- ❌ `download (3).jpg`

## Tracking Credits

Update `image-credits.json` when adding images:

```json
{
  "filename": "family-pool.jpg",
  "path": "images/unsplash/family-pool.jpg",
  "credit": "Photo by Jane Smith",
  "creditUrl": "https://unsplash.com/@janesmith",
  "altText": "Family splashing in cruise ship pool",
  "usage": ["families.html - hero section"],
  "license": "Unsplash License"
}
```

## Legal Compliance

### Unsplash
- ✅ Free to use
- ✅ No permission needed
- ✅ Commercial use allowed
- ⚠️ Credit appreciated (not required, but good practice)
- ❌ Don't compile into stock photo site

### Cruise Line Media
- ✅ Use images provided through partner portal
- ✅ Keep logos/watermarks intact
- ⚠️ Only use for promoting their cruises
- ❌ Don't use for non-cruise products
- ❌ Don't modify embedded branding

## Quick Reference: Adding Image to Page

```html
<!-- Link the credits CSS in <head> -->
<link rel="stylesheet" href="css/image-credits.css">

<!-- Hero image with overlay credit -->
<section class="hero hero-image-container">
  <img src="images/cruise-lines/royal-caribbean/ship.jpg" 
       alt="Royal Caribbean cruise ship">
  <span class="image-credit">
    Courtesy of <a href="https://www.royalcaribbean.com">Royal Caribbean</a>
  </span>
  <div class="hero-content">
    <h1>Your Content Here</h1>
  </div>
</section>

<!-- Gallery image with caption credit -->
<div class="gallery-item">
  <img src="images/unsplash/sunset.jpg" 
       alt="Caribbean sunset cruise">
  <span class="image-credit">
    Photo by <a href="https://unsplash.com/@photographer">John Doe</a> on Unsplash
  </span>
</div>
```

## Need Help?

- Bulk image optimization: I can create a Python script
- Batch credit addition: I can create a PowerShell script
- Converting images to WebP: I can set up automation
- Credits page: I can create a dedicated credits/about page
