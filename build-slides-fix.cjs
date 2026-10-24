const fs = require("fs");
const path = require("path");

const WS = process.argv[2] || process.cwd();
const root = path.join(WS, "frontend");
const outDir = path.join(root, "dist-slides");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// 1. Read index.html head
const idx = fs.readFileSync(path.join(root, "index.html"), "utf8");
const headM = idx.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
let head = headM ? headM[1].replace(/<script[\s\S]*?<\/script>/gi, "").replace(/<!--[\s\S]*?-->/g, "").trim() : "";

// 2. Read CSS from vite build output
const artDir = path.join(WS, "artifacts", "assets");
let css = "";
if (fs.existsSync(artDir)) {
  const f = fs.readdirSync(artDir).find(function(f) { return f.endsWith(".css"); });
  if (f) css = fs.readFileSync(path.join(artDir, f), "utf8");
}
if (!css) {
  const mp = path.join(root, "src", "styles", "main.css");
  if (fs.existsSync(mp)) css = fs.readFileSync(mp, "utf8");
}

// 3. Read all slide-N.js and extract HTML
const slidesDir = path.join(root, "src", "slides");
const files = fs.readdirSync(slidesDir)
  .filter(function(f) { return /^slide-\d+\.js$/.test(f); })
  .sort(function(a, b) { return parseInt(a.match(/\d+/)[0]) - parseInt(b.match(/\d+/)[0]); });

var bodies = [];
for (var fi = 0; fi < files.length; fi++) {
  var f = files[fi];
  var c = fs.readFileSync(path.join(slidesDir, f), "utf8");
  var m = c.match(/window\.slideDataMap\.set\(\d+,\s*`([\s\S]*?)`\s*\);/);
  if (m) {
    var html = m[1].trim();
    html = html.replace(/(<div)([\s>])/, '$1 class="slide-page"$2');
    bodies.push(html);
  }
}

// 4. Copy assets
var assetsSrc = path.join(root, "public", "assets");
var assetsDest = path.join(outDir, "assets");
if (fs.existsSync(assetsSrc)) fs.cpSync(assetsSrc, assetsDest, { recursive: true });

// 5. Write all-slides.html
var allHtml = '<!DOCTYPE html><html><head>' + head + '<style>' + css + '</style></head><body>\n' + bodies.join('\n\n') + '\n</body></html>';
fs.writeFileSync(path.join(outDir, "all-slides.html"), allHtml);

// 6. Write individual slide-N.html
for (var i = 0; i < bodies.length; i++) {
  var h = '<!DOCTYPE html><html><head>' + head + '<style>' + css + '</style></head><body>' + bodies[i] + '</body></html>';
  fs.writeFileSync(path.join(outDir, "slide-" + i + ".html"), h);
}

console.log("Done: " + bodies.length + " slides, CSS " + css.length + " bytes, output: " + outDir);
