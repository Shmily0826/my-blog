import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../public/demos/sky-scout');
const info = JSON.parse(fs.readFileSync(path.join(root, 'build-info.json'), 'utf8'));
assert.equal(info.sourceCommit, '4fdf1ac943992b8fd5934145b35d734212906123');
for (const relative of info.files) {
  const target = path.resolve(root, relative);
  assert(target.startsWith(root + path.sep), 'Runtime file escapes the demo directory');
  assert(fs.statSync(target).size > 0, `Missing/empty runtime file: ${relative}`);
}
function files(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(directory, entry.name);
    return entry.isDirectory() ? files(target) : [target];
  });
}
for (const file of files(root)) {
  assert(!['.env', 'flutter_service_worker.js'].includes(path.basename(file)), 'Private config or service worker was packaged');
  assert(!file.endsWith('.map') && !file.endsWith('.symbols'), 'Debug artifacts were packaged');
}
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
assert(html.includes('<base href="/demos/sky-scout/">'));
assert(html.includes('content="noindex"'));
const bootstrap = fs.readFileSync(path.join(root, 'flutter_bootstrap.js'), 'utf8');
assert(bootstrap.includes("canvasKitBaseUrl: '/demos/sky-scout/canvaskit/'"));
assert(bootstrap.includes("canvasKitVariant: 'full'"));
assert(fs.statSync(path.join(root, 'canvaskit/canvaskit.wasm')).size > 1000000);
const fonts = JSON.parse(fs.readFileSync(path.join(root, 'assets/FontManifest.json'), 'utf8'));
assert(fonts.some((family) => family.family === 'DemoRoboto'));
for (const family of fonts) for (const font of family.fonts) {
  assert(fs.existsSync(path.join(root, 'assets', font.asset)), `Missing font ${font.asset}`);
}
for (const filename of ['ATTRIBUTION.txt', 'ROBOTO-LICENSE.txt', 'assets/NOTICES']) {
  assert(fs.statSync(path.join(root, filename)).size > 0);
}
for (const filename of ['stars.json', 'constellation_western.json']) {
  const data = JSON.parse(fs.readFileSync(path.join(root, 'assets/assets/data', filename), 'utf8'));
  assert(Object.keys(data).length > 0);
}
console.log(`Sky demo package check passed: ${info.files.length} runtime files, local engine/fonts/catalogs, attribution, no credentials or debug artifacts.`);
