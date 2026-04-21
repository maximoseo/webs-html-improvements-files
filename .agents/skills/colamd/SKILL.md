# SKILL: ColaMD
**Source:** https://github.com/marswaveai/ColaMD
**Domain:** code
**Trigger:** When needing a Markdown editor that auto-refreshes in real time as an AI agent edits the file — for live pair programming with agents

## Summary
ColaMD is an Electron-based WYSIWYG Markdown editor built for agent-native workflows. It uses `fs.watch` to detect changes from any AI agent (Claude Code, Cursor, Copilot) and refreshes instantly with an activity indicator showing when agents are writing.

## Key Patterns
- `fs.watch` auto-refresh with agent activity indicator (orange pulse while active, green when done)
- True WYSIWYG — type Markdown, see rich text; no split-pane preview
- Cross-platform: macOS (.dmg), Windows (.exe), Linux (.AppImage/.deb)
- Built on Electron + Milkdown (ProseMirror) + TypeScript + electron-vite
- 4 built-in themes + custom CSS import; PDF/HTML export
- No cloud sync, no plugin system — intentionally minimal

## Usage
Download from GitHub Releases, open any `.md` file, let your agent edit it.
Stack: `npm install && npm run dev` to build from source.

## Code/Template
```bash
# Build from source
git clone https://github.com/marswaveai/colamd.git
cd colamd && npm install && npm run dev
# Distribution builds
npm run dist:mac / dist:win / dist:linux
```
