"""投稿素材批量截图：
1) 7 类型 × 合拢/展开 静帧（本地 three 版 _verify-c3，稳定快）
2) 剖面 1 张
3) 真身 CDN 版：流心奶黄"展开解构 + 转盘"过渡 GIF（连续帧 PIL 合成）
输出目录 post-assets/
"""
import sys, time, os
from playwright.sync_api import sync_playwright
from PIL import Image

BASE_LOCAL = "http://127.0.0.1:8931/_verify-c3.html"
BASE_REAL  = "http://127.0.0.1:8931/demo-C3-%E6%9C%88%E9%A5%BC3D.html"   # 真身（CDN 版）
OUT = "post-assets"
os.makedirs(OUT, exist_ok=True)
NAMES = ["lotus", "five", "bean", "custard", "taro", "rose", "su"]
CN = {0:"广式莲蓉蛋黄",1:"经典五仁",2:"豆沙月饼",3:"流心奶黄",4:"冰皮芋泥",5:"玫瑰鲜花",6:"苏式枣泥"}

t0 = time.time()
def log(*a): print("[%.1f]" % (time.time()-t0), *a, flush=True)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width":1024,"height":900})
    pg.on("pageerror", lambda e: log("PAGEERR", str(e)[:200]))

    # ---- A. 静帧 14 张 + 剖面 1 张（本地版）----
    for i in range(7):
        for mode, qs, tag in [("collapsed", f"static=1&type={i}", "合拢"),
                              ("exploded",  f"static=1&explode=1&type={i}", "展开")]:
            url = f"{BASE_LOCAL}?{qs}"
            pg.goto(url, wait_until="commit", timeout=60000)
            try:
                pg.wait_for_function("() => window.__settled === true", timeout=90000)
            except Exception as e:
                log("settle fail", i, mode, repr(e)[:120])
            pg.wait_for_timeout(700)
            out = f"{OUT}/s{i:02d}-{NAMES[i]}-{mode}.png"
            pg.screenshot(path=out, timeout=40000)
            log("SHOT", out)
    # 剖面（莲蓉，点击剖切按钮）
    pg.goto(f"{BASE_LOCAL}?static=1&type=0", wait_until="commit", timeout=60000)
    try:
        pg.wait_for_function("() => window.__ready === true", timeout=120000)
        pg.click("#sectionBtn", timeout=8000)
        pg.wait_for_function("() => window.__settled === true", timeout=60000)
    except Exception as e:
        log("section fail", repr(e)[:160])
    pg.wait_for_timeout(800)
    pg.screenshot(path=f"{OUT}/s70-lotus-section.png", timeout=40000)
    log("SHOT section")

    # ---- B. 真身 CDN 版：流心奶黄 展开过程 GIF 帧 ----
    pg2 = b.new_page(viewport={"width":640,"height":560})
    pg2.on("pageerror", lambda e: log("REAL PAGEERR", str(e)[:200]))
    pg2.goto(f"{BASE_REAL}?explode=1&type=3", wait_until="commit", timeout=60000)
    try:
        pg2.wait_for_function("() => window.__ready === true", timeout=180000)
    except Exception as e:
        log("REAL ready fail", repr(e)[:160])
    frames = []
    for k in range(18):
        png = pg2.screenshot(timeout=40000)
        f = f"{OUT}/gif-{k:02d}.png"
        with open(f, "wb") as fp: fp.write(png)
        frames.append(f)
        pg2.wait_for_timeout(220)
    pg2.screenshot(path=f"{OUT}/s80-custard-real.png", timeout=40000)
    log("REAL frames done")
    try: b.close()
    except Exception: pass

# ---- C. PIL 合成 GIF（缩小到 512 宽，控制体积）----
imgs = [Image.open(f).convert("P", palette=Image.ADAPTIVE) for f in frames]
w0 = imgs[0].width
scale = 512 / w0
imgs = [im.resize((int(im.width*scale), int(im.height*scale))) for im in imgs]
imgs[0].save(f"{OUT}/explode-custard.gif", save_all=True, append_images=imgs[1:], duration=220, loop=0)
log("GIF -> %s (%.0f KB)" % (f"{OUT}/explode-custard.gif", os.path.getsize(f"{OUT}/explode-custard.gif")/1024))
for f in frames: os.remove(f)
log("ALL DONE")
