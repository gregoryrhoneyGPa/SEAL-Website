const fs = require('fs').promises;
const path = require('path');
const sharp = require('sharp');

const originalsDir = path.join(__dirname, '..', 'images', 'canva', 'originals');
const outDir = path.join(__dirname, '..', 'images', 'canva', 'optimized');
const reportPath = path.join(outDir, 'report.json');

const sizes = [1920, 1200, 800, 400];
const formats = [
  { ext: 'webp', opts: { quality: 80 } },
  { ext: 'avif', opts: { quality: 50 } },
  // keep a reasonably-compressed jpeg/png fallback
  { ext: 'jpg', opts: { quality: 75 } }
];

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

function isImageFile(name) {
  return /\.(jpe?g|png|webp|avif)$/i.test(name);
}

async function statSafe(p) {
  try { return await fs.stat(p); } catch (e) { return null; }
}

async function optimizeFile(fileName) {
  const srcPath = path.join(originalsDir, fileName);
  const base = path.parse(fileName).name.replace(/\s+/g, '-').toLowerCase();
  const meta = await sharp(srcPath).metadata();
  const originalStat = await statSafe(srcPath);
  const result = { file: fileName, originalSize: originalStat ? originalStat.size : null, originalWidth: meta.width || null, outputs: [] };

  for (const width of sizes) {
    if (meta.width && width > meta.width) continue; // skip upscales
    for (const fmt of formats) {
      const outName = `${base}-${width}.${fmt.ext}`;
      const outPath = path.join(outDir, outName);
      try {
        let pipeline = sharp(srcPath).resize({ width, withoutEnlargement: true });
        if (fmt.ext === 'webp') pipeline = pipeline.webp(fmt.opts);
        else if (fmt.ext === 'avif') pipeline = pipeline.avif(fmt.opts);
        else if (fmt.ext === 'jpg') pipeline = pipeline.jpeg(fmt.opts);

        await pipeline.toFile(outPath);
        const st = await statSafe(outPath);
        result.outputs.push({ path: path.relative(path.join(__dirname, '..'), outPath), size: st ? st.size : null, width, format: fmt.ext });
      } catch (err) {
        console.error('Failed to process', srcPath, err.message);
      }
    }
  }

  // also write a responsibly-compressed full-width webp if original is smaller than largest size
  const largestOut = path.join(outDir, `${base}-orig.webp`);
  try {
    await sharp(srcPath).webp({ quality: 80 }).toFile(largestOut);
    const st = await statSafe(largestOut);
    result.outputs.push({ path: path.relative(path.join(__dirname, '..'), largestOut), size: st ? st.size : null, width: meta.width || null, format: 'webp' });
  } catch (err) {
    console.error('Failed to write orig.webp for', srcPath, err.message);
  }

  return result;
}

async function run() {
  console.log('Scanning', originalsDir);
  await ensureDir(outDir);
  const names = await fs.readdir(originalsDir);
  const images = names.filter(isImageFile);
  const results = [];
  for (const img of images) {
    console.log('Optimizing', img);
    const r = await optimizeFile(img);
    results.push(r);
  }
  await fs.writeFile(reportPath, JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 2));
  console.log('Done. Report written to', reportPath);
}

run().catch(err => { console.error(err); process.exit(1); });
