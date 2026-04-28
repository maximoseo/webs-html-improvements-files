# Agent 2b — CSS Applicator Memo

Role: Apply design tokens mechanically. No creative decisions.

## Cost Tier
Mid (GPT 5.5 or GPT 4o-mini). ~90% cheaper than Opus for same CSS volume.

## Trigger
Called after Agent 2 produces design tokens JSON, or when cached tokens exist.

## Input
- HTML skeleton from Agent 1
- Design tokens JSON (from Agent 2 or cache)

## Output
Same HTML with inline CSS applied.

## Optimization
- Never called if tokens unchanged and skeleton structure identical.
- Cache output by hash(html+tokens) using response-cache.py.
