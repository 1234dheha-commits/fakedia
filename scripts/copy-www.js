const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const www = path.join(root, 'www');
fs.mkdirSync(www, { recursive: true });

for (const file of ['index.html', 'manifest.json']) {
  const src = path.join(root, file);
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(www, file));
}
console.log('www/ updated from project root');
