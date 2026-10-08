#!/usr/bin/env python3
"""一键跑通无头数值验证：生成离线验证页 -> 起本地服务 -> 跑 ?verifyall=1 断言。

用法:
    python verify.py                 # 默认端口 8931
    python verify.py --port 9000      # 换端口
    python verify.py --url <url>      # 直接打已有服务，跳过起服务

依赖见 requirements.txt；首次使用需: python -m playwright install chromium
退出码: 断言全过(输出含 VERIFY-SUMMARY ... ALL-OK) 返回 0，否则返回 1。
"""
import argparse
import functools
import http.server
import os
import subprocess
import sys
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
VERIFY_PAGE = "_verify-c3.html"


def gen_verify_page():
    subprocess.run([sys.executable, os.path.join(ROOT, "_mkverify.py")], cwd=ROOT, check=True)
    if not os.path.exists(os.path.join(ROOT, VERIFY_PAGE)):
        sys.exit("未生成 %s（_mkverify.py 未产出？）" % VERIFY_PAGE)


def serve(port):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    ap = argparse.ArgumentParser(description="一键跑无头数值验证")
    ap.add_argument("--port", type=int, default=8931)
    ap.add_argument("--url", default=None, help="已有服务地址；给出则跳过本地起服务")
    args = ap.parse_args()

    httpd = None
    if args.url:
        target = args.url
    else:
        gen_verify_page()
        httpd = serve(args.port)
        target = "http://127.0.0.1:%d/%s?static=1&verifyall=1" % (args.port, VERIFY_PAGE)

    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(ROOT, "_verify_run.py"), target],
            cwd=ROOT, capture_output=True, text=True,
        )
    finally:
        if httpd is not None:
            httpd.shutdown()

    sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)

    ok = ("VERIFY-SUMMARY" in proc.stdout) and ("ALL-OK" in proc.stdout)
    print("\n[verify.py] %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
