#!/usr/bin/env python3
"""Tiny static server for the code screensaver.

Usage:
    python3 server.py [ROOT_DIR] [--port 8777]

Serves the screensaver page at http://localhost:PORT/ and exposes:
    GET /api/files       -> JSON list of code files under ROOT_DIR
    GET /file?path=REL   -> raw text of one file (must live under ROOT_DIR)
"""
import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

HERE = os.path.dirname(os.path.abspath(__file__))

CODE_EXT = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".rb", ".go",
    ".rs", ".java", ".kt", ".swift", ".c", ".h", ".cc", ".cpp", ".hpp",
    ".cs", ".php", ".sh", ".zsh", ".bash", ".lua", ".sql", ".html", ".css",
    ".scss", ".sass", ".vue", ".svelte", ".json", ".yml", ".yaml", ".toml",
    ".md", ".ex", ".exs", ".clj", ".hs", ".ml", ".r", ".dart", ".scala",
}
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt", "out",
    "vendor", "__pycache__", ".venv", "venv", "coverage", ".cache",
    ".turbo", "target", "bin", "obj", ".idea", ".vscode",
}
# Skip absurdly large or minified files.
MAX_BYTES = 200_000


def find_asset_dir():
    """Locate @highlightjs/cdn-assets in node_modules — searching this dir and
    upward, so it works whether npm installed locally (standalone laptop clone)
    or hoisted to a monorepo root (wedops workspace)."""
    d = HERE
    while True:
        cand = os.path.join(d, "node_modules", "@highlightjs", "cdn-assets")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.join(HERE, "node_modules", "@highlightjs", "cdn-assets")
        d = parent


ASSET_DIR = find_asset_dir()


def collect_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in CODE_EXT:
                continue
            if ".min." in name:
                continue
            full = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(full)
            except OSError:
                continue
            if size == 0 or size > MAX_BYTES:
                continue
            files.append(os.path.relpath(full, root))
    files.sort()
    return files


class Handler(BaseHTTPRequestHandler):
    root = os.getcwd()

    def log_message(self, *args):
        pass  # keep the terminal quiet — this is a screensaver

    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
            return

        if path.startswith("/vendor/"):
            base = ASSET_DIR
            full = os.path.normpath(os.path.join(base, path[len("/vendor/"):]))
            if not full.startswith(os.path.abspath(base) + os.sep):
                self._send(403, "forbidden")
                return
            ctype = ("text/css; charset=utf-8" if full.endswith(".css")
                     else "application/javascript; charset=utf-8" if full.endswith(".js")
                     else "application/octet-stream")
            try:
                with open(full, "rb") as f:
                    self._send(200, f.read(), ctype)
            except OSError:
                self._send(404, "vendor asset not found — run: npm install")
            return

        if path == "/api/files":
            self._send(200, json.dumps(collect_files(self.root)), "application/json")
            return

        if path == "/file":
            rel = unquote(parse_qs(parsed.query).get("path", [""])[0])
            full = os.path.normpath(os.path.join(self.root, rel))
            # Prevent path traversal outside root.
            if not full.startswith(os.path.abspath(self.root) + os.sep):
                self._send(403, "forbidden")
                return
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as f:
                    self._send(200, f.read())
            except OSError:
                self._send(404, "not found")
            return

        self._send(404, "not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=os.getcwd(), help="directory of code to display")
    ap.add_argument("--port", type=int, default=8777)
    args = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")

    Handler.root = root
    count = len(collect_files(root))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"code screensaver: {count} files under {root}")
    print(f"open  ->  http://localhost:{args.port}/   (then fullscreen: Cmd+Shift+F / F11)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
