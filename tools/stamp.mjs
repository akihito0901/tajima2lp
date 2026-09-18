/**
 * index.html の画像・動画のURLに、中身のハッシュを `?v=` として押し直す。
 *
 * なぜ要るか：
 * `assets/images/` のファイルは名前が固定なので、中身だけ差し替えるとURLが変わらない。
 * ブラウザやCDNが古い方を持っていると、デプロイしても差し替わって見えない。
 * URLにハッシュを付けておけば、内容が変わった瞬間に別URLになるので必ず取り直される。
 *
 * そのうえで `_headers` と `vercel.json` で `/assets/images/*` を1年 immutable に
 * しているため、**ハッシュを押し忘れると更新が永遠に届かない。**
 * 手で書かずに必ずこのスクリプトを通すこと。デプロイ手順に組み込んである。
 *
 *   node tools/stamp.mjs
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const htmlPath = join(root, 'index.html');

const hashOf = (rel) =>
  createHash('md5').update(readFileSync(join(root, rel))).digest('hex').slice(0, 8);

let html = readFileSync(htmlPath, 'utf8');
const missing = [];
const stamped = new Map();

// ./assets/images/xxx.webp か ./assets/images/xxx.mp4 を拾う。
// 既に ?v=... が付いていれば押し直す。
html = html.replace(
  /\.\/assets\/images\/([A-Za-z0-9._-]+)(\?v=[0-9a-f]+)?/g,
  (whole, name) => {
    const rel = `assets/images/${name}`;
    if (!existsSync(join(root, rel))) {
      missing.push(rel);
      return whole;
    }
    const h = hashOf(rel);
    stamped.set(name, h);
    return `./assets/images/${name}?v=${h}`;
  }
);

writeFileSync(htmlPath, html);

for (const [name, h] of [...stamped].sort()) console.log(`  ${name}  ?v=${h}`);
if (missing.length) {
  console.error('\n参照されているのに実体が無いファイル:');
  for (const m of missing) console.error('  ' + m);
  process.exit(1);
}
console.log(`\n${stamped.size} 件にハッシュを押した`);
