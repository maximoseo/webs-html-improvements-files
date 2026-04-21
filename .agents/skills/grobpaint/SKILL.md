# SKILL: GrobPaint
**Source:** https://github.com/groverburger/grobpaint
**Domain:** code
**Trigger:** When needing a lightweight cross-platform image editor with layers, or building a Python+vanilla JS desktop app with pywebview

## Summary
A lightweight multiplatform image editor (between MS Paint and Paint.NET) built with Python backend and vanilla JS frontend. Features layers, 16 blend modes, selection tools, adjustments with live preview, and a PWA mode. No npm, no bundler required.

## Key Patterns
- Python + pywebview for native window (falls back to browser if not installed)
- Pure vanilla JS frontend with ES modules — no build step, no npm
- `python grobpaint.py` to launch; `--browser` flag for browser-only mode
- PWA-capable: can be installed from browser and works offline
- `.gbp` project format preserves layers as a ZIP archive
- Auto-save to localStorage
- Sprite sheet support: split/export layers as horizontal sheet
- 16 blend modes per layer, per-layer opacity
- Build standalone app: `./build.sh` → PyInstaller produces `.app` (macOS) or binary
- Dependencies: Python 3.9+, optional `pywebview`

## Usage
Clone, run `python grobpaint.py`. Open index.html directly for browser-only mode (no file dialogs). Build distributable with `./build.sh`. Install pywebview for native window: `pip install pywebview`.

## Code/Template
```bash
# Run from source (native window)
pip install pywebview
python grobpaint.py

# Force browser mode
python grobpaint.py --browser

# Build standalone app
./build.sh
# → dist/GrobPaint.app (macOS) or dist/GrobPaint/GrobPaint (Linux/Windows)

# Serve index.html for browser-only use
python -m http.server 8080  # then open http://localhost:8080
```
