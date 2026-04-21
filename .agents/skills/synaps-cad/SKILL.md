# SKILL: SynapsCAD — AI-Powered 3D CAD IDE
**Source:** https://github.com/ierror/synaps-cad
**Domain:** creative-tools
**Trigger:** Use when editing 3D CAD models with natural language, generating or modifying OpenSCAD code via AI chat, or building an AI-assisted 3D design workflow with real-time preview.

## Summary
SynapsCAD is a desktop Rust/Bevy 3D CAD application combining an OpenSCAD code editor, real-time 3D viewport, and AI chat assistant. Write OpenSCAD code, compile to 3D geometry, then instruct AI to modify models via natural language including 3D click context.

## Key Patterns
- AI sees current code + part labels from 3D click interactions
- Multi-provider AI support: Anthropic, OpenAI, Gemini, Groq, DeepSeek, Cohere, Ollama (local/offline)
- Compile: scad-rs parser → csgrs CSG geometry → Bevy 3D viewport
- Pre-built binaries for Linux, macOS (Apple Silicon + Intel), Windows
- macOS unsigned: `sudo xattr -rd com.apple.quarantine /path/to/SynapsCAD.app`
- Build from source: `cargo run`

## Usage
When user wants to "vibe code" 3D models using AI — describe modifications in chat, see changes in real-time viewport.

## Code/Template
```bash
# Download from releases page or build:
export ANTHROPIC_API_KEY="sk-..."
cargo run

# Workflow:
# 1. Write/edit OpenSCAD code in editor panel
# 2. Click Compile → 3D model renders
# 3. Ask AI: "Make the base 20% wider and add rounded corners"
# 4. AI updates code → re-compile → preview
```
