const fs = require('fs');
const path = require('path');
const input = process.argv[2] || path.join(__dirname, '..', 'images', 'canva', 'optimized', 'report.json');
const output = process.argv[3] || path.join(__dirname, '..', 'images', 'canva', 'optimized', 'summary.csv');

try {
  const raw = fs.readFileSync(input, 'utf8');
  const data = JSON.parse(raw);
  const rows = [];
  rows.push(['file','originalSize','bestOptimizedSize','bestFormat','bestPath','savingsBytes','savingsPercent']);
  let totalOrig = 0;
  let totalOpt = 0;

  for (const item of data.results) {
    const orig = item.originalSize || 0;
    totalOrig += orig;
    let best = null;
    if (Array.isArray(item.outputs)) {
      for (const o of item.outputs) {
        if (!best || (o.size || Infinity) < (best.size || Infinity)) best = o;
      }
    }
    const bestSize = best ? (best.size || 0) : 0;
    totalOpt += bestSize;
    const save = orig - bestSize;
    const pct = orig > 0 ? ((save / orig) * 100).toFixed(1) : '0.0';
    rows.push([item.file, orig, bestSize, best ? best.format : '', best ? best.path.replace(/\\/g, '/') : '', save, pct]);
  }

  const totalSave = totalOrig - totalOpt;
  const totalPct = totalOrig > 0 ? ((totalSave / totalOrig) * 100).toFixed(1) : '0.0';
  rows.push(['TOTAL', totalOrig, totalOpt, '', '', totalSave, totalPct]);

  const csv = rows.map(r => r.map(cell => {
    if (typeof cell === 'string' && cell.includes(',')) return `"${cell}"`;
    return cell;
  }).join(',')).join('\n');

  fs.writeFileSync(output, csv, 'utf8');
  console.log('Wrote', output);
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}
