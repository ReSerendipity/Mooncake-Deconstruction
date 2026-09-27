// 用法: node check_syntax.js demo.html
// 抽取 <script type="module"> 的模块体，剥掉 import 行后用 new Function 校验语法。
const fs = require('fs');
const path = process.argv[2];
if (!path) { console.log('usage: node check_syntax.js <file.html>'); process.exit(1); }
const html = fs.readFileSync(path, 'utf8');
const all = [...html.matchAll(/<script type="module">([\s\S]*?)<\/script>/g)];
if (!all.length) { console.log('NO MODULE SCRIPT FOUND'); process.exit(1); }
let bad = 0;
all.forEach((m, idx) => {
  let body = m[1];
  body = body.replace(/^\s*import[\s\S]*?from\s+['"][^'"]+['"];?\s*$/gm, '');
  body = body.replace(/^\s*import\s+['"][^'"]+['"];?\s*$/gm, '');
  try {
    new Function(body);
    console.log(`SYNTAX OK  (module #${idx}, ${body.length} chars)`);
  } catch (e) {
    console.log(`SYNTAX ERROR (module #${idx}): ${e.message}`);
    bad++;
  }
});
process.exit(bad ? 2 : 0);
