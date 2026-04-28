# Agent 5 Local — Mechanical Integrator Memo

Role: Variable substitution, UTM tagging, tracking pixel, metadata. Zero API cost.

## Cost Tier
Free. Local Python script.

## Trigger
Called for EVERY run except when smart decisions (conditionals, A/B) are explicitly requested.

## Input
- Optimized HTML from Agent 4
- Variable map (default or custom JSON)
- Campaign ID
- Tracking pixel URL

## Output
Production-ready HTML with n8n expressions, UTM params, tracking pixel, version metadata.

## Validation
- Checks malformed n8n expressions
- Warns if over Gmail 102KB limit
- Warns if over 80KB soft target

## Optimization
- Skips Agent 5-AI (GLM) entirely for standard runs.
- GLM only called if user explicitly requests conditional logic or A/B variant design.
