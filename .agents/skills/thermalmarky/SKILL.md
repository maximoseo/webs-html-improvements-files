# SKILL: ThermalMarky — Markdown Thermal Printer
**Source:** https://github.com/sadreck/ThermalMarky
**Domain:** developer-tools
**Trigger:** Use when printing Markdown content to thermal receipt printers, setting up print-from-web workflows, or building physical output from AI-generated content via CLI or HTTP API.

## Summary
ThermalMarky converts Markdown to ESC/POS commands for thermal printers, with a web UI and CLI. Supports headers, bold, underline, lists, center/left/right alignment, QR codes, horizontal lines. Docker-ready, configurable via env vars.

## Key Patterns
- Supports USB (vendor/product ID) and network (IP:port) printer connections
- Custom tags: `[align=center]`, `[qr=https://...]`, `[effect=line--]`
- CLI: `python print.py my_list.md` or `echo "# Hello" | python print.py`
- HTTP: `curl -X POST http://localhost:8000/print --data-urlencode "markdown@file.md"`
- Docker: `docker compose up --build` → UI at `https://localhost:8000`
- Max lines configurable to avoid runaway prints

## Usage
When user has a thermal printer and wants to print formatted content from AI output, scripts, or a web UI.

## Code/Template
```markdown
[align=center]# Receipt

Item 1: **$10.99**
Item 2: __important__

[effect=line--]
[align=center]Total: $10.99

[qr=https://example.com]
```
