import sys, time
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "collapsed"
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
    pg = b.new_page(viewport={"width": 1024, "height": 900})
    pg.on("console", lambda m: log("CONSOLE", m.type, m.text[:300]))
    pg.on("pageerror", lambda e: log("PAGEERR", str(e)[:400]))
    log("GOTO", url)
    pg.goto(url, wait_until="commit", timeout=60000)
    log("COMMIT")
    try:
        pg.wait_for_function("() => window.__ready === true", timeout=120000)
        log("READY ok")
    except Exception as e:
        log("READY fail", repr(e)[:160])
    if "explode" in url:
        try:
            pg.wait_for_function("() => window.__settled === true", timeout=60000)
            log("SETTLED (auto-explode)")
        except Exception as e:
            log("settle fail", repr(e)[:160])
    if mode == "exploded":
        try:
            pg.click("#toggle", timeout=8000)
            log("clicked toggle")
            pg.wait_for_function("() => window.__settled === true", timeout=60000)
            log("SETTLED ok")
        except Exception as e:
            log("explode fail", repr(e)[:200])
    pg.wait_for_timeout(900)
    pg.screenshot(path=out, timeout=40000)
    log("SHOT done in %.1fs" % (time.time()-t0))
    b.close()
