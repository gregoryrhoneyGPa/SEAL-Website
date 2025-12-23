#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
function walk(dir){
  return fs.readdirSync(dir, {withFileTypes:true}).flatMap(d=>{
    const p = path.join(dir,d.name);
    if(d.isDirectory()) return walk(p);
    if(/\.html?$/.test(d.name)) return [p];
    return [];
  });
}

const files = walk(root);
let changed = 0;
files.forEach(file=>{
  let s = fs.readFileSync(file,'utf8');
  const orig = s;
  // Add loading="lazy" to <img> tags that don't already have loading attribute
  s = s.replace(/<img((?![^>]*\bloading=)[^>]*?)>/gi, (m, g1)=>{
    // if img already has width/height and likely hero, skip only if loading already present is handled above
    return `<img${g1} loading="lazy">`;
  });
  if(s !== orig){ fs.writeFileSync(file,s,'utf8'); changed++; }
});
console.log(`Processed ${files.length} files, updated ${changed} files.`);
