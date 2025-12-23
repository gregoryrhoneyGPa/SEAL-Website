Canva → SEAL site workflow

1) Exporting images from Canva
- Choose JPG or PNG. For photos use JPG (quality 80-90). For graphics with transparency use PNG.
- Recommended sizes (px): hero 1600×800, feature cards 1200×800, thumbnails 800×800 or 600×400 depending on layout.
- Download at 72–150 DPI for web; a higher DPI is unnecessary and increases file size.
- Name files with lowercase, hyphens: e.g. mediterranean-1.jpg
- Compress after download using https://squoosh.app or ImageOptim / `magick` (ImageMagick):

  magick input.jpg -strip -quality 82 -resize 1600x1600\> output.jpg

2) Updating images in the repo
- Replace files in the `images/` folder with the exported images using the same filename, or update the `src` in the HTML to the new filename.
- For multiple sizes, you can add `-large`, `-thumb` suffixes and update markup to use `srcset` for responsive images.
- Add/update `alt` text in the HTML for each image to describe the photo (important for accessibility and SEO).

3) Updating text
- For small text changes, open the relevant HTML file (`Index.html`, `about.html`, etc.) and edit the text nodes directly.
- For repeated content blocks, consider maintaining a simple `partials/` folder and using a basic build script later.

4) Embeds vs exported images
- Canva can provide an Embed (iframe) for designs; you can paste the iframe into the HTML, but iframes have accessibility and performance trade-offs.
- Recommended: export optimized images from Canva and add them to the `images/` folder (best for performance and SEO).

5) Practical checklist before committing
- Run `tools/basic_a11y_check.py` to catch missing `alt`, `lang`, or heading issues.
- Verify images are < 300 KB where possible; hero images up to ~500 KB are acceptable if compressed.
- Test on mobile and desktop.

6) If you want, I can:
- Replace selected images for you in the repo (you can upload the exported images here), or
- Create an automated script to optimize and rename Canva exports into the `images/` folder.
