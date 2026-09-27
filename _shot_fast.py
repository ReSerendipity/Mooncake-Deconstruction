"""快速迭代：只截莲蓉 合拢/展开/剖面 3 张，用于自检外观。"""
import sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8931/_verify-c3.html"
SHOTS = [
    ("iter-lotus",    f"{BASE}?static=1&type=0",            "collapsed"),
    ("iter-exploded", f"{BASE}?static=1&explode=1&type=0",  "auto"),
    ("iter-section",  f"{BASE}?static=1&type=0",            "section"),
]
# 命令行可覆盖：python _shot_fast.py "<suffix>" "<querystring>"
if len(sys.argv) >= 3:
    sfx = sys.argv[1]; qs = sys.argv[2]
    SHOTS = [(sfx, f"{BASE}?static=1&{qs}", "auto")]

t0 = time.time()
def log(*a): print("[%.1f]" % (time.time() - t0), *a, flush=True)

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
        if mode == "auto":
            try:
                pg.wait_for_function("() => window.__settled === true", timeout=90000)
            except Exception as e:
                log("settle fail", repr(e)[:160])
        if mode == "section":
            try:
                pg.click("#sectionBtn", timeout=8000)
                pg.wait_for_function("() => window.__settled === true", timeout=60000)
            except Exception as e:
                log("section settle fail", repr(e)[:160])
        pg.wait_for_timeout(900)
        out = f"shot-{name}.png"
        pg.screenshot(path=out, timeout=40000)
        log("SHOT", out)
    log("ALL DONE")
sys.stdout.flush()
import os
os._exit(0)
