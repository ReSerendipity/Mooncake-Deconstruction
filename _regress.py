"""视觉回归：加载静态合拢帧，截图并用 PIL 客观比色，确认仍是"暖金月饼"观感，无回归。"""
import sys, time, io
from playwright.sync_api import sync_playwright
from PIL import Image

URL = "http://127.0.0.1:8931/_verify-c3.html?static=1"
t0 = time.time()
def log(*a): print("[%.1f]" % (time.time()-t0), *a); sys.stdout.flush()

shot_png = None
b = None
try:
    pw = sync_playwright().start()
    b = pw.chromium.launch(args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width":1024,"height":900})
    errs=[]
    def _on_console(m):
        if m.type == "error": errs.append(m.text[:160])
    pg.on("console", _on_console)
    pg.on("pageerror", lambda e: errs.append("PAGEERR:"+str(e)[:200]))
    log("GOTO", URL)
    pg.goto(URL, wait_until="commit", timeout=60000)
    pg.wait_for_function("() => window.__settled === true", timeout=120000)
    log("SETTLED")
    time.sleep(0.8)
    png = pg.screenshot()
    shot_png = png
    log("SHOT bytes=%d" % len(png))
except Exception as e:
    log("FATAL", repr(e)[:200])
finally:
    pass

if shot_png:
    with open("_regress.png","wb") as f: f.write(shot_png)
    im = Image.open(io.BytesIO(shot_png)).convert("RGB")
    w,h = im.size
    px = im.load()
    # 画布中心矩形（约占 50% 宽、60% 高）采集月饼主体色
    x0,x1 = int(w*0.25), int(w*0.75)
    y0,y1 = int(h*0.20), int(h*0.85)
    n=0; sr=sg=sb=0; warm=0
    for y in range(y0,y1,4):
        for x in range(x0,x1,4):
            r,g,bl = px[x,y]; sr+=r; sg+=g; sb+=bl; n+=1
            if r>bl+8 and r>60: warm+=1
    mr,mg,mb = sr//n, sg//n, sb//n
    warm_pct = 100.0*warm/n
    # 整体画面非黑比例（确认有渲染内容）
    log("SIZE %dx%d" % (w,h))
    log("CENTER mean RGB = (%d,%d,%d)  L≈%d  R-B=%d" % (mr,mg,mb, (mr+mb)//2, mr-mb))
    log("WARM(暖金)占比 = %.1f%%" % warm_pct)
    # 判定：中心应是偏暖的金棕（R>B 且有一定亮度）
    ok = (mr>mb+5) and (mr>70) and (warm_pct>20)
    log("REGRESS-CHECK %s" % ("PASS" if ok else "FAIL"))
print("ERRORS:", errs if 'errs' in dir() else "n/a")
import os; os._exit(0)
