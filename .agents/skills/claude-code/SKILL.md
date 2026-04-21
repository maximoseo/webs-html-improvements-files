# SKILL: Claw Code (Rust CLI Agent)
**Source:** https://github.com/instructkr/claude-code
**Domain:** code
**Trigger:** When needing a Rust-based open-source CLI agent harness compatible with Anthropic/OpenAI APIs

## Summary
Claw Code is the public Rust implementation of the `claw` CLI agent harness — a build-from-source alternative that drives LLMs via API key (not subscription login). Includes a parity harness for comparing behavior against reference implementations.

## Key Patterns
- Single binary `claw` built from `rust/` workspace
- Requires ANTHROPIC_API_KEY (or OPENAI_API_KEY), not subscription login
- `claw doctor` — health check; `claw prompt "..."` — run a prompt
- Session management and parity testing built-in
- Windows: use `claw.exe` with PowerShell

## Usage
```bash
git clone https://github.com/ultraworkers/claw-code
cd claw-code/rust && cargo build --workspace
export ANTHROPIC_API_KEY="sk-ant-..."
./target/debug/claw doctor
./target/debug/claw prompt "say hello"
```

## Code/Template
```powershell
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
.\target\debug\claw.exe prompt "say hello"
```
