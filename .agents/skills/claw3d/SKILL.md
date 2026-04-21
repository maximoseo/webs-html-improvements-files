# SKILL: Claw3D
**Source:** https://github.com/iamlukethedev/Claw3D
**Domain:** code
**Trigger:** When building a 3D visualization layer for AI agent workflows or wanting to monitor agents in an immersive office environment

## Summary
Claw3D is a Next.js + Three.js frontend that renders a 3D retro office where AI agents appear as workers. It connects to OpenClaw, Hermes, or custom backends to provide live agent monitoring, chat, approvals, and GitHub review flows.

## Key Patterns
- Gateway-first architecture: browser connects to Studio, Studio connects to upstream WebSocket gateway
- Runtime providers: OpenClaw, Hermes, Demo mode, Custom HTTP backend
- Custom runtime needs: GET /health, GET /state, GET /registry, POST /v1/chat/completions
- Same-origin WebSocket proxy avoids browser CORS issues
- Tech: Next.js App Router, React Three Fiber, Three.js, Drei, TypeScript

## Usage
```bash
git clone <repo> claw3d && cd claw3d
npm install && cp .env.example .env && npm run dev
# Demo mode (no backend):
npm run demo-gateway && npm run dev
```
Connect at http://localhost:3000, configure gateway URL/token in Studio settings.

## Code/Template
```bash
# Demo mode for exploring without a real agent backend
npm run demo-gateway
npm run dev
# Connect to ws://localhost:18789 in Studio, choose "Demo backend"
```
