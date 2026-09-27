"""一次性在同一浏览器里截 4 张图（广式莲蓉 / 苏式，合拢 / 展开）。"""
import sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8931/_verify-c3.html"
SHOTS = [
    # 展开态一律用 URL 上的 ?explode=1 自动展开；mode 用 "auto" 表示不要再去点 #toggle
    # （点 #toggle 会触发合拢动画，而页面 __settled 未复位会导致截到中间帧）
    ("lotus-collapsed", f"{BASE}?static=1&type=0", "collapsed"),
    ("lotus-exploded",  f"{BASE}?static=1&explode=1&type=0", "auto"),
    ("su-collapsed",    f"{BASE}?static=1&type=6", "collapsed"),
    ("su-exploded",     f"{BASE}?static=1&explode=1&type=6", "auto"),
]
t0 = time.time()
def log(*a): print("[%.1f]" % (time.time()-t0), *a, flush=True)

with sync_playwright() as p:
    b = p.chromium.launch(args=[
        "--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
    ])
    pg = b.new_page(viewport={"width": 1024, "height": 900})
    pg.on("pageerror", lambda e: log("PAGEERR", str(e)[:300]))
    for name, url, mode in SHOTS:
        log("GOTO", name, url)
        pg.goto(url, wait_until="commit", timeout=60000)
        try:
            pg.wait_for_function("() => window.__ready === true", timeout=120000)
        except Exception as e:
            log("READY fail", repr(e)[:160])
        if "explode" in url:
            try:
                pg.wait_for_function("() => window.__settled === true", timeout=60000)
            except Exception as e:
                log("settle fail", repr(e)[:160])
        # 展开态也可点一下保险
        if mode == "exploded":
            try:
                pg.click("#toggle", timeout=8000)
                pg.wait_for_function("() => window.__settled === true", timeout=60000)
            except Exception:
                pass
        pg.wait_for_timeout(900)
        out = f"final-c3-{name}.png"
        pg.screenshot(path=out, timeout=40000)
        log("SHOT", out)
    # 不要在 SwiftShader 下调用 b.close()——它会挂住永不返回，直接退出进程
log("ALL DONE")
sys.stdout.flush()
import os
os._exit(0)
