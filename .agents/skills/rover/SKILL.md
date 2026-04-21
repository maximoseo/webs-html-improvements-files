# SKILL: Rover - DOM-Native AI Execution Engine for Websites
**Source:** https://github.com/rtrvr-ai/rover
**Domain:** code
**Trigger:** When embedding AI agent capabilities into websites, enabling AI-driven web automation via DOM, or building agent-accessible web interfaces

## Summary
DOM-native execution engine that turns any website into an AI-native interface. Reads the live page, plans actions, and executes directly in the browser without screenshots or VMs. Exposes task API at POST /v1/tasks and supports WebMCP discovery.

## Key Patterns
- Direct DOM + accessibility tree reading (no screenshots/pixels)
- Millisecond latency (in-browser, not remote VM)
- RoverBook analytics: visit replays, agent reviews, agent memory
- WebMCP task/tools discovery for AI agent access
- Well-known discovery: /.well-known/rover-site.json, /.well-known/agent-card.json
- Script tag or npm installation

## Usage
```html
<script type="application/agent+json">{"task":"https://agent.rtrvr.ai/v1/tasks"}</script>
<script>
  rover('boot', { siteId: 'YOUR_SITE_ID', publicKey: 'pk_site_...', allowedDomains: ['yourdomain.com'] });
</script>
<script src="https://rover.rtrvr.ai/embed.js?v=YOUR_SITE_KEY_ID" async></script>
```

## Code/Template
```typescript
import { boot } from "@rtrvr-ai/rover";
const rover = boot({ siteId: "YOUR_SITE_ID", publicKey: "pk_site_...", allowedDomains: ["yourdomain.com"] });
// AI agents access via: POST https://agent.rtrvr.ai/v1/tasks
```
