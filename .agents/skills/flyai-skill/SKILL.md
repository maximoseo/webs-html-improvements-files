# SKILL: FlyAI — Travel, Flight & Hotel Search (Fliggy/Alibaba)
**Source:** https://github.com/alibaba-flyai/flyai-skill
**Domain:** marketing
**Trigger:** Use when searching flights, hotels, trains, attractions, or travel products via natural language inside an AI agent terminal, especially for China/Asia travel via Fliggy (Alibaba).

## Summary
FlyAI connects AI agents (Claude Code, OpenClaw) to Fliggy's travel platform (Alibaba Group) for real-time flight, hotel, train, attraction, and concert searches. Returns structured JSON with direct booking links. Eight specialized commands, optional API key.

## Key Patterns
- `flyai keyword-search --query "things to do in Tokyo"` — broad discovery
- `flyai ai-search --query "romantic beach resort for anniversary"` — semantic search
- `flyai search-flight --origin BEJ` — structured flight search
- `flyai search-hotel --city Shanghai --checkin 2025-08-01` — hotel search
- Results include direct booking links and structured JSON
- Install: `npm i -g @fly-ai/flyai-cli` then `npx skills add alibaba-flyai/flyai-skill`

## Usage
When user needs real-time travel inventory search within an agent conversation, especially Fliggy/China-market travel. Works without API key for basic queries.

## Code/Template
```bash
npm i -g @fly-ai/flyai-cli
npx skills add alibaba-flyai/flyai-skill

flyai keyword-search --query "boutique hotels in Kyoto"
flyai search-flight --origin SHA --destination PEK
flyai ai-search --query "family resort with water park under $200"
```
