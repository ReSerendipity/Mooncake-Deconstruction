// 通用 HTML script 语法检查（覆盖普通 script + module script）
const fs = require('fs');
let bad = 0;
for (const file of process.argv.slice(2)) {
  const html = fs.readFileSync(file, 'utf8');
  const all = [...html.matchAll(/<script(?:\s+type="module")?>([\s\S]*?)<\/script>/g)];
  if (!all.length) { console.error('NO SCRIPT FOUND: ' + file); process.exit(1); }
  all.forEach((m, idx) => {
    let body = m[1];
    body = body.replace(/^\s*import[\s\S]*?from\s+['"][^'"]+['"];?\s*$/gm, '');
    body = body.replace(/^\s*import\s+['"][^'"]+['"];?\s*$/gm, '');
    try { new Function(body); console.log(`SYNTAX OK ${file} (script #${idx})`); }
    catch (e) { console.error(`SYNTAX ERROR ${file} (#${idx}): ${e.message}`); bad++; }
  });
}
process.exit(bad ? 2 : 0);
