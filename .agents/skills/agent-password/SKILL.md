# SKILL: Agent Password - Local macOS Password Manager for Agents
**Source:** https://github.com/tartavull/agent-password
**Domain:** code
**Trigger:** When managing secrets for AI agent workflows, providing secure credential access to agents with human approval, or building Touch ID-gated secret sharing systems

## Summary
Local macOS password manager CLI for agent workflows. Secrets encrypted with XChaCha20-Poly1305 in SQLite vault. Touch ID unlocks vault key. Agents request secrets by ID, humans approve subsets. Both humans and agents use same CLI.

## Key Patterns
- Shared session model: one session per macOS user, agents request from it
- Secrets expose only metadata until approved (agents see IDs, not plaintext)
- Numbered approval: approve `all` or `1,4,3-6` subset
- Approved secrets readable until `session clear` or `session close`
- XChaCha20-Poly1305 encryption, macOS keychain for vault key

## Usage
```bash
cargo install --path .
agent-password vault init
agent-password session create
agent-password secrets list                    # Agent sees metadata only
agent-password secrets request github --requester codex --reason "repo setup"
agent-password requests approve 1 all          # Human approves with Touch ID
agent-password secrets get github --json       # Agent reads approved secret
agent-password session close
```

## Code/Template
```bash
# Add a secret
printf '%s\n' 'my-password' | agent-password login add github \
  --username myuser --url https://github.com --password-stdin --tag work
```
