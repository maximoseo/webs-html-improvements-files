# KWR Agent Prompt — Open Questions

These items remain underspecified and should be confirmed before running evals
or deploying the KWR pipeline in production.

## Injection Point
- [ ] Confirm whether KWR-AGENT-PROMPT.md should live in AGENTS.md, .hermes.md, or another injection point; that choice affects precedence and how much identity/tone should live here versus in SOUL.md.

## Clarification Surface
- [ ] Confirm whether AskUserQuestion is a real project wrapper around Hermes clarification or whether the runtime should use native clarify (currently assumed: native clarify).

## UI Contracts
- [ ] Confirm whether the exact UI labels, placeholders, and color palette are contractual requirements or illustrative examples.

## Row / Pillar / Cluster Precedence
- [ ] Confirm which rule has precedence when row-count (200-250), pillar-count (10-15), and cluster-count (10-15 per pillar) requirements conflict. Currently: return honest lower count with explanation rather than padding.

## Language Handling
- [ ] Confirm how language auto-detection should behave for mixed-language sites, especially when Hebrew content and English brand terms coexist.

## Test Commands
- [ ] Confirm the canonical repo test commands and smoke-test entrypoints, rather than assuming only one command path.

## Sample Files
- [ ] Confirm whether referenced sample .xlsx files are actually available to the agent for format comparison or whether they are only examples named in the spec.

## Connection Test Scope
- [ ] Confirm whether the connection test must prove write capability or only spreadsheet reachability before enabling Run.

## Webhook Auth Contract
- [ ] Confirm the exact webhook auth, retry, and payload contract for deployment through the configured n8n integration path.

## Slug / Worksheet Name Normalization
- [ ] Confirm the normalization rules for worksheet names and slugs when brand names include non-ASCII text (e.g. Hebrew characters).
