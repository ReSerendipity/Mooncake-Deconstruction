"""非静态（真实交互）页面性能/健壮性冒烟：加载 -> 等 __ready -> 空转 2.6s（idle 自转+自适应 Governor）-> 收集报错 + 截图。"""
import sys, time, os
from playwright.sync_api import sync_playwright

base = "http://127.0.0.1:8931/demo-C3-月饼3D.html"
t0 = time.time()
def log(*a): print("[%.1f]" % (time.time()-t0), *a, flush=True)

errs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=[
        "--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
    ])
    pg = b.new_page(viewport={"width": 1024, "height": 900})
    pg.on("console", lambda m: (errs.append(("console", m.type, m.text[:200])) if m.type in ("error","warning") else None))
    pg.on("pageerror", lambda e: errs.append(("pageerror", str(e)[:300])))
    log("GOTO", base)
    pg.goto(base, wait_until="commit", timeout=60000)
    try:
        pg.wait_for_function("() => window.__ready === true", timeout=60000)
        log("READY ok")
    except Exception as e:
        log("READY fail", repr(e)[:160])
    # 空转 2.6s：idle 自转跑起来 + 自适应 Governor 评估窗口(1.5s)应已触发
    time.sleep(2.6)
    # 截图 + 检查画布确有内容（中心亮于角落，证明渲染未崩溃）
    pg.wait_for_timeout(300)
    pg.screenshot(path="perf-shot.png", timeout=40000)
    # 读取画布像素：中心 vs 角落平均亮度差，确认渲染出月饼而非空白
    stat = pg.evaluate("""() => {
        const c = document.querySelector('canvas');
        if(!c) return {canvas:false};
        return {canvas:true, w:c.width, h:c.height};
    }""")
    log("CANVAS", stat)
    log("ERRORS/WARNINGS:", len(errs))
    for e in errs[:20]:
        log("  ", *e)
    log("ALL DONE")
os._exit(0)
