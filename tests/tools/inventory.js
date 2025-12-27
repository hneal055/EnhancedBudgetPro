// tools/inventory.js
const fs = require('fs');
const path = require('path');

const root = process.cwd();
const ignore = ['node_modules', '.git', '.vscode', 'dist', 'build'];

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries.flatMap(e => {
    const full = path.join(dir, e.name);
    if (ignore.includes(e.name)) return [];
    if (e.isDirectory()) {
      return [{ type: 'dir', path: path.relative(root, full) }].concat(walk(full));
    } else {
      const ext = path.extname(e.name).toLowerCase();
      return [{
        type: 'file',
        path: path.relative(root, full),
        name: e.name,
        ext,
        size: fs.statSync(full).size,
        mtime: fs.statSync(full).mtimeMs
      }];
    }
  });
}

const all = walk(root);

// Heuristics for relevance to Enhanced Budget Pro
const relevancePatterns = [
  /budget/i,
  /template/i,
  /schema/i,
  /report/i,
  /payroll/i,
  /schedule/i,
  /cost/i,
  /invoice/i,
  /\.json$/,
  /\.csv$/,
  /\.xlsx$/,
  /\.xls$/,
  /\.py$/,
  /\.js$/,
  /\.ts$/,
  /\.md$/
];

function isRelevant(item) {
  if (item.type === 'dir') return relevancePatterns.some(r => r.test(item.path));
  return relevancePatterns.some(r => r.test(item.path) || r.test(item.name));
}

const relevant = all.filter(isRelevant);
const manifest = {
  generatedAt: new Date().toISOString(),
  root,
  counts: { total: all.length, relevant: relevant.length },
  relevant
};

fs.mkdirSync('tools', { recursive: true });
fs.writeFileSync('inventory.json', JSON.stringify(manifest, null, 2));
console.log('Inventory written to inventory.json');
