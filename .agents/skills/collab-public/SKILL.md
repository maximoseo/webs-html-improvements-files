# SKILL: Collaborator
**Source:** https://github.com/collaborator-ai/collab-public
**Domain:** code
**Trigger:** When needing an infinite-canvas desktop environment for running multiple AI agents alongside code files and terminals

## Summary
A native desktop app (Electron 40 + React 19) for agentic development on an infinite canvas. Terminals, context files, and running code arranged side-by-side. Supports macOS, Windows (PowerShell + WSL2), and Linux. All data stored locally.

## Key Patterns
- Infinite pan-and-zoom canvas with tile-based layout (terminal, note, code, image tiles)
- Terminal tiles backed by persistent node-pty sidecar sessions
- Monaco Editor for code, BlockNote/TipTap for rich markdown editing
- File tiles bound to disk paths — auto-reload on external changes
- All state stored in `~/.collaborator/` as JSON
- D3 force-directed graph for relationship visualization
- Drag files from navigator onto canvas to create tiles
- Double-click empty canvas space to create a terminal tile
- Zoom 33-100%, snap to grid

## Usage
Download latest release for your OS. Add workspace via Cmd+Shift+O. Double-click canvas for terminal. Drag files from navigator. Use Cmd+K for search. Terminal working directory set to active workspace path.

## Code/Template
```json
// Canvas state format (~/.collaborator/canvas-state.json)
{
  "version": 1,
  "tiles": [{
    "id": "tile-<timestamp>-<index>",
    "type": "term | note | code | image",
    "x": 0, "y": 0, "width": 440, "height": 540,
    "filePath": "/absolute/path/to/file",
    "zIndex": 1
  }]
}
```
