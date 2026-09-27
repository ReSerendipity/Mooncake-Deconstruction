import re, sys, pathlib
src = pathlib.Path("demo-C3-月饼3D.html").read_text(encoding="utf-8")
src = src.replace("https://unpkg.com/three@0.160.0/build/three.module.js", "./three.module.local.js")
src = src.replace("https://unpkg.com/three@0.160.0/examples/jsm/", "./addons/")
pathlib.Path("_verify-c3.html").write_text(src, encoding="utf-8")
print("wrote _verify-c3.html", len(src), "chars")
