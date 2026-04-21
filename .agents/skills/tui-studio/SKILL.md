# SKILL: TUI Studio (Visual TUI Editor)
**Source:** https://github.com/jalonsogo/tui-studio
**Domain:** design
**Trigger:** When building terminal UIs, designing CLI layouts visually, or creating TUI-based interfaces for Python/Rust/Go apps

## Summary
A Figma-like visual editor for designing Terminal User Interface (TUI) layouts. Drag-and-drop widgets onto a terminal canvas, set colors/borders/layout, then export as code for Textual (Python), Ratatui (Rust), or other TUI frameworks.

## Key Patterns
- **Visual-first design**: Design TUIs with a GUI, not by guessing character coordinates
- **Framework export**: Exports to Textual (Python), Ratatui (Rust), Bubbletea (Go), Blessed (Node.js)
- **Widget palette**: Panels, tables, progress bars, input fields, menus, charts, status bars
- **Layout system**: Grid-based, percentage or fixed character dimensions
- **Color picker**: Full 256-color and truecolor support with terminal compatibility preview
- **Border styles**: Single, double, rounded, thick, ASCII-compatible fallbacks

## Usage
Open TUI Studio → drag widgets onto canvas → configure properties → export code.

Use when an agent needs to implement terminal dashboards, monitoring UIs, data entry forms, or interactive CLI tools.

## Code/Template
```python
# Generated Textual app (Python)
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, ProgressBar
from textual.containers import Container, Horizontal

class MyTUI(App):
    CSS = """
    Container { layout: grid; grid-size: 2; }
    DataTable { height: 100%; border: round $accent; }
    ProgressBar { width: 100%; }
    """
    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield DataTable()
            with Horizontal():
                yield ProgressBar(total=100)
        yield Footer()

if __name__ == "__main__":
    MyTUI().run()
```
```rust
// Generated Ratatui layout (Rust)
use ratatui::{layout::{Constraint, Direction, Layout}, widgets::{Block, Borders, Table}};

fn render(frame: &mut Frame) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([Constraint::Min(0), Constraint::Length(3)])
        .split(frame.size());
    
    frame.render_widget(
        Block::default().title("Dashboard").borders(Borders::ALL),
        chunks[0]
    );
}
```
