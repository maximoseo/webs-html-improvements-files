# SKILL: filenotes.nvim — Per-File Notes in Neovim
**Source:** https://github.com/UsamaQaisrani/filenotes.nvim
**Domain:** code
**Trigger:** When you want per-file markdown notes in a floating window inside Neovim, scoped to project root

## Summary
Neovim plugin that opens a per-file markdown note in a floating window. Notes stored in .notes/ at project root (identified by hash of file path). No database — just markdown files.

## Key Patterns
- Notes scoped to project root (git root or cwd fallback)
- Keymap: <leader>nn (configurable)
- Window size configurable (width/height as % of editor)
- Recommend adding .notes/ to global .gitignore

## Usage
Use for adding context, TODOs, or AI agent instructions to specific files in a project.

## Code/Template
```lua
-- lazy.nvim
{
  "UsamaQaisrani/filenotes.nvim",
  config = function()
    require("filenotes").setup({
      keymap = "<leader>nn",
      window_width = 0.6,
      window_height = 0.6,
    })
  end
}
-- Press <leader>nn to open note for current file
-- echo ".notes/" >> ~/.gitignore_global
```
