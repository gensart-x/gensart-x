const fs = require('fs');

const FILE = 'README.md';

let content = fs.readFileSync(FILE, 'utf-8');

const start = '<!--START_SECTION-->';
const end = '<!--END_SECTION-->';

const newData = `Last updated: ${new Date().toISOString()}`;

// find positions
const startIndex = content.indexOf(start);
const endIndex = content.indexOf(end);

if (startIndex !== -1 && endIndex !== -1) {
  const before = content.slice(0, startIndex + start.length);
  const after = content.slice(endIndex);

  content = `${before}\n${newData}\n${after}`;
} else {
  // fallback if markers missing
  content += `\n\n${start}\n${newData}\n${end}\n`;
}

fs.writeFileSync(FILE, content);
