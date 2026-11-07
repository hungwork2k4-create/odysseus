import assert from 'node:assert/strict';
<<<<<<< HEAD
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const markdownPath = path.join(__dirname, '..', 'static', 'js', 'markdown.js');
let src = fs.readFileSync(markdownPath, 'utf8');

src = src.replace(
  /import uiModule from '\.\/ui\.js';/,
  'const uiModule = { esc: (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\\"/g, "&quot;") };'
);
src = src.replace(
  /import \{ splitTableRow \} from '\.\/markdown\/tableRow\.js';/,
  'const splitTableRow = (row) => row.split("|").filter((cell) => cell.trim() !== "");'
);
src = src.replace(/export function /g, 'function ');
src = src.replace(/export const /g, 'const ');
src = src.replace(/export default markdownModule;?/g, '');
src += '\nthis.__mdToHtml = mdToHtml;';

class MutationObserver {
  observe() {}
  disconnect() {}
}

const sandbox = {
  console,
  URL,
  MutationObserver,
  localStorage: { getItem() { return '[]'; }, setItem() {} },
  document: {
    body: { classList: { contains() { return true; } } },
    addEventListener() {},
    querySelectorAll() { return []; },
    getElementById() { return null; },
    contains() { return true; },
  },
  window: {
    location: { origin: 'http://localhost' },
    katex: null,
    mermaid: null,
  },
};

vm.createContext(sandbox);
vm.runInContext(src, sandbox, { filename: markdownPath });
=======
import { loadMarkdown } from './streaming/markdownHarness.mjs';

// Use the same ES-module loader as the streaming renderer tests. It keeps the
// production exports intact and handles the browser's versioned sibling imports.
const { mdToHtml } = await loadMarkdown();
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483

const input = [
  '> ```html',
  '> <script>',
  '>   newWindow.addEventListener(\'click\', () => {',
  '>     desktop.appendChild(newWindow);',
  '>   });',
  '> </script>',
  '> ```',
].join('\n');

<<<<<<< HEAD
const html = sandbox.__mdToHtml(input);
=======
const html = mdToHtml(input);
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
assert.equal(html.includes('___ALLOWED_HTML_'), false, html);
assert.equal(html.includes('appendChild'), true, html);

console.log('ok');
