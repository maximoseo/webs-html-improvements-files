# SKILL: Project N.O.M.A.D. — Offline Knowledge Server
**Source:** https://github.com/Crosstalk-Solutions/project-nomad
**Domain:** knowledge-management
**Trigger:** Use when setting up an offline-first self-contained knowledge/education server with AI chat, offline Wikipedia, maps, and courses — ideal for remote/emergency preparedness scenarios.

## Summary
Project N.O.M.A.D. (Node for Offline Media, Archives, and Data) is a self-hosted offline server with AI chat (Ollama+RAG), Wikipedia via Kiwix, Khan Academy via Kolibri, offline maps via ProtoMaps, CyberChef, and note-taking. Managed via Docker Compose with a web UI.

## Key Patterns
- One-line install on Debian/Ubuntu: `curl -fsSL <install-url> | sudo bash`
- Browse at `http://localhost:8080`
- AI chat with local Ollama or OpenAI-compatible APIs + Qdrant vector search
- Offline Wikipedia, medical references, survival guides via Kiwix
- Khan Academy courses with progress tracking via Kolibri
- Downloadable regional maps via ProtoMaps

## Usage
When setting up offline knowledge infrastructure for remote sites, disaster preparedness, or air-gapped environments. Requires beefy hardware for AI features.

## Code/Template
```bash
sudo apt-get update && sudo apt-get install -y curl && \
curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/install_nomad.sh \
  -o install_nomad.sh && sudo bash install_nomad.sh
# Access at http://localhost:8080
```
