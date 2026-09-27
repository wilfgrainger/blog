import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

let sharp;
try {
  ({ default: sharp } = await import('sharp'));
} catch (error) {
  const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
  if (!runtimeModules) throw new Error('Install the sharp Node package to export SVGs.', { cause: error });
  const require = createRequire(pathToFileURL(path.join(runtimeModules, '_resolver.cjs')));
  sharp = require('sharp');
}

const articleDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const imagesDir = path.join(articleDir, 'images');
for (const file of (await fs.readdir(imagesDir)).filter(file => /^0[2-4]-.*\.svg$/.test(file)).sort()) {
  const target = file.replace(/\.svg$/, '.png');
  const png = await sharp(path.join(imagesDir, file), { density: 144 }).png({ compressionLevel: 9 }).toBuffer();
  const temporary = path.join(imagesDir, `${target}.tmp`);
  await fs.writeFile(temporary, png);
  await fs.rename(temporary, path.join(imagesDir, target));
  console.log(`Exported ${target}`);
}
