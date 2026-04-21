---
name: Bash Security Analysis
description: Shell obfuscation detection, terminal workflow analysis, and secure bash handling.
color: "#475569"
emoji: 🛡️
vibe: Audit the script before it runs.
---

# Bash Security Analysis Skill

Synthesized from `Bashfuscator/Bashfuscator`.

## 🧠 Core Capabilities
- **Obfuscation Awareness:** Detects payload hiding, variable expansion tricks, and malicious bash execution patterns.
- **Secure Execution:** Reviews shell scripts for injection vulnerabilities and unquoted variables before execution.

## 🎯 When to Use
- When auditing a new repository's build scripts or `Makefile`.
- When an agent needs to execute an unknown or complex bash command safely.

## 🚨 Anti-Patterns
- Do not use for frontend / HTML redesign tasks. Keep shell analysis isolated to backend infrastructure and CI/CD jobs.
