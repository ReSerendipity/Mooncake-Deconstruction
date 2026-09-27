"""跑页面自报的数值断言（?verifyall=1），收集 console 里的 VERIFY| 行。
用法:
    python verify_run.py [url]        # 默认 http://127.0.0.1:8931/_verify.html?static=1&verifyall=1
前提: 页面已实现 window.__verifyDone 与 console.log('VERIFY|' + JSON.stringify(...))
输出建议重定向到文件后读取（管道缓冲会吞输出）:
    python verify_run.py > verify.out 2>&1
"""
import sys, time, json, os
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8931/_verify.html?static=1&verifyall=1"
t0 = time.time()
def log(*a): print("[%.1f]" % (time.time() - t0), *a); sys.stdout.flush()

rows, summary = [], None
b = None
try:
    pw = sync_playwright().start()
    b = pw.chromium.launch(args=[
        "--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
    ])
    pg = b.new_page(viewport={"width": 1024, "height": 900})
    def on_console(m):
        global summary
        t = m.text
        if t.startswith("VERIFY|"): rows.append(t[7:])
        elif t.startswith("VERIFY-SUMMARY"): summary = t
        elif m.type == "error": log("CONSOLE-ERR", t[:200])
    pg.on("console", on_console)
    pg.on("pageerror", lambda e: log("PAGEERR", str(e)[:300]))
    log("GOTO", url)
    pg.goto(url, wait_until="commit", timeout=60000)
    try:
        pg.wait_for_function("() => window.__verifyDone === true", timeout=240000)
        log("VERIFY DONE")
    except Exception as e:
        log("VERIFY wait fail", repr(e)[:160])
except Exception as e:
    log("FATAL", repr(e)[:200])

print("\n=== 类型 / 状态 / 屏幕NDC包围盒 / 世界高度 / fit / struct ===")
for r in rows:
    try:
        d = json.loads(r)
        print("%-12s %-9s ndcX[%6.3f,%6.3f] ndcY[%6.3f,%6.3f]  worldY[%5.3f,%5.3f]  fit=%-5s struct=%-5s"
              % (d.get('t', '?'), d.get('st', '?'), d['ndcX'], d['ndcX2'],
                 d['ndcY'], d['ndcY2'], d['worldY'], d['worldY2'], d['fit'], d['structOK']))
    except Exception as e:
        print("PARSE FAIL", r[:200], e)
print("\nSUMMARY:", summary)
print("rows: %d  elapsed %.1fs" % (len(rows), time.time() - t0))
sys.stdout.flush()
# 注意：不要 b.close()。SwiftShader 下 close() 可能长时间挂住，导致外层任务永不返回。
# 直接 os._exit 结束进程，残留的 chrome-headless-shell 由调用方 taskkill 清理。
os._exit(0)
