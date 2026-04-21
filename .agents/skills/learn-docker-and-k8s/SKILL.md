# SKILL: Learn Docker and K8s
**Source:** https://github.com/ericboy0224/learn-docker-and-k8s
**Domain:** code
**Trigger:** When learning Docker and Kubernetes through interactive AI-driven scenarios, or teaching DevOps fundamentals via a game-based approach

## Summary
An open-source interactive learning game where your AI editor becomes a mentor ("Sarah") and walks you through 7 real-world DevOps scenarios — from containers to Kubernetes production incidents. Type "let's play" to start.

## Key Patterns
- Works with any AI editor: Claude Code, Cursor, Windsurf, Copilot, Cline, Codex, Gemini CLI
- 7 chapters: containers → images → storage → networks → Docker Compose → Kubernetes → production
- Narrative-driven: NoCappuccino Inc. startup context with characters (Sarah, Dave, Marcus)
- Commands: `/play`, `/env-check`, `/progress`, `/hint`, `/verify`, `/next`
- Difficulty levels; `/hint` has 3 nudge levels
- Naturally covers Linux fundamentals (namespaces, cgroups) and networking (DNS, NAT, iptables)
- Prerequisites: Docker, Docker Compose v2, an AI editor

## Usage
Clone repo, open in AI editor, type "let's play". AI reads game files, becomes Sarah, walks through challenges. Verify solutions with `/verify`, get nudges with `/hint`.

## Code/Template
```bash
git clone https://github.com/ericboy0224/learn-docker-and-k8s.git
cd learn-docker-and-k8s
# Open in Claude Code, Cursor, etc., then type:
# "let's play"

# Or use slash commands:
# /play          - start/resume
# /env-check     - verify Docker setup
# /hint          - get a nudge (3 levels)
# /verify        - check your solution
```
