import sys, time, os
from playwright.sync_api import sync_playwright

base = "http://127.0.0.1:8931/demo-C3-月饼3D.html"
t0 = time.time()
def log(*a): print("[%.1f]" % (time.time()-t0), *a); sys.stdout.flush()

with sync_playwright() as p:
    b = p.chromium.launch(args=[
        "--no-sandbox",
        "--use-gl=angle",
        "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader",
        "--ignore-gpu-blocklist",
    ])
    for tag, q in [("collapsed", "?static=1"), ("exploded", "?static=1&explode=1")]:
        pg = b.new_page(viewport={"width": 1024, "height": 900})
        pg.on("console", lambda m, t=tag: log(t, "CONSOLE", m.type, m.text[:200]))
        pg.on("pageerror", lambda e, t=tag: log(t, "PAGEERR", str(e)[:300]))
        url = base + q
        log(tag, "GOTO", url)
        pg.goto(url, wait_until="commit", timeout=60000)
        try:
            pg.wait_for_function("() => window.__ready === true", timeout=120000)
            log(tag, "READY ok")
        except Exception as e:
            log(tag, "READY fail", repr(e)[:160])
        try:
            pg.wait_for_function("() => window.__settled === true", timeout=60000)
            log(tag, "SETTLED ok")
        except Exception as e:
            log(tag, "settle fail", repr(e)[:160])
        pg.wait_for_timeout(700)
        out = "cdn-%s.png" % tag
        pg.screenshot(path=out, timeout=40000)
        log(tag, "SHOT", out)
        pg.close()
    # never b.close() under swiftshader — it hangs; just exit the process
    os._exit(0)
