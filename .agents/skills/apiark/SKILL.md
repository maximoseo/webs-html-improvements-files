# SKILL: ApiArk
**Source:** https://github.com/berbicanes/apiark
**Domain:** code
**Trigger:** When building or testing APIs, replacing Postman/Insomnia, or needing a lightweight local-first API client

## Summary
A Tauri v2-based API client (~60 MB RAM vs Postman's 800 MB) that supports REST, GraphQL, gRPC, WebSocket, SSE, and MQTT. All data stored as plain YAML files for git-friendly workflows. No login, no cloud.

## Key Patterns
- Filesystem-based storage (YAML files, git-diffable, no lock-in)
- Multi-protocol: REST, GraphQL, gRPC, WebSocket, SSE, MQTT, Socket.IO
- TypeScript scripting: `ark.test()`, `ark.expect()`, `ark.env.set()`
- Local mock servers with Faker.js, latency simulation, error injection
- Cron-based local monitoring with desktop notifications
- OpenAPI editor with Spectral linting
- One-click import from Postman, Insomnia, Bruno, Hoppscotch, HAR, cURL
- AI assistant for natural language to requests + auto-generate tests

## Usage
Import existing Postman collections (v2.1 JSON) via Ctrl+K > "Import Collection". Collections become YAML directories you own. Use TypeScript pre/post-request scripts for automation. Run collection suites with CSV/JSON data files.

## Code/Template
```yaml
# users/create-user.yaml
name: Create User
method: POST
url: "{{baseUrl}}/api/users"
headers:
  Content-Type: application/json
body:
  json:
    name: "{{$faker.name}}"
```
