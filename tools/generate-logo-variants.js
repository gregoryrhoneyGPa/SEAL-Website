const path = require('path');
const fs = require('fs').promises;
const sharp = require('sharp');

const repoRoot = path.join(__dirname, '..');
const imagesDir = path.join(repoRoot, 'images');

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function generate() {
  await ensureDir(imagesDir);

  const logoSvg = path.join(imagesDir, 'seal-logo.svg');
  const markSvg = path.join(imagesDir, 'seal-mark.svg');

  // header sizes
  const header = { w1: 280, h1: 60 };
  const header2 = { w2: header.w1 * 2, h2: header.h1 * 2 };

  // footer/mark sizes
  const mark1 = 36;
  const mark2 = 72;

  async function genFromSvg(svgPath, outBase, sizes) {
    const results = [];
    for (const s of sizes) {
      const { name, width, height, ext, opts } = s;
      const out = path.join(imagesDir, `${outBase}-${name}.${ext}`);
      try {
        let pipeline = sharp(svgPath).resize({ width, height, fit: 'contain' });
        if (ext === 'webp') pipeline = pipeline.webp(opts || { quality: 80 });
        else if (ext === 'png') pipeline = pipeline.png(opts || { compressionLevel: 9 });
        else if (ext === 'jpeg' || ext === 'jpg') pipeline = pipeline.jpeg(opts || { quality: 80 });

        await pipeline.toFile(out);
        results.push(out);
      } catch (err) {
        console.error('Failed to write', out, err.message);
      }
    }
    return results;
  }

  console.log('Generating header variants...');
  await genFromSvg(logoSvg, 'seal-logo-horizontal-280', [
    { name: '280', width: header.w1, height: header.h1, ext: 'png' },
    { name: '560', width: header2.w2, height: header2.h2, ext: 'png' },
    { name: '280', width: header.w1, height: header.h1, ext: 'webp' },
    { name: '560', width: header2.w2, height: header2.h2, ext: 'webp' }
  ]);

  console.log('Generating mark variants...');
  await genFromSvg(markSvg, 'seal-mark', [
    { name: '36', width: mark1, height: mark1, ext: 'png' },
    { name: '72', width: mark2, height: mark2, ext: 'png' },
    { name: '36', width: mark1, height: mark1, ext: 'webp' },
    { name: '72', width: mark2, height: mark2, ext: 'webp' }
  ]);

  console.log('Logo variants generated in images/');
}

generate().catch(err => { console.error(err); process.exit(1); });
