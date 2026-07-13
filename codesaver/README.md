# codesaver

A passive code "screensaver" — it page-flips through a folder of your source
files with syntax highlighting. Reads well on a 13" laptop and a 50" wall alike
(font size scales with the viewport). Installed by the [`mac`](../mac) bootstrap,
which symlinks the `codesaver` command onto your `PATH`.

## Run

```bash
codesaver ~/wedops          # any folder; defaults to the current directory
codesaver ~/thc/admin --port 9000
```

It opens your browser to the screensaver and starts paging. Fullscreen with
`Cmd+Ctrl+F` (or F11). `Ctrl+C` in the terminal stops it.

- **`T`** — cycle syntax themes (remembered across sessions)
- **any other key / click** — skip to the next page

## How it works

A tiny Python server (`server.py`) walks the folder for code files (skipping
`node_modules`, `.git`, build output, minified and oversized files), and the
page (`index.html`) fetches them one screenful at a time. Syntax highlighting is
[highlight.js](https://highlightjs.org), vendored offline via
`@highlightjs/cdn-assets` (`npm install` — the only dependency). Runs entirely
on `127.0.0.1`; nothing leaves the machine.
