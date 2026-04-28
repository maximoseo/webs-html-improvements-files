# Dashboard Data Contract

Endpoint: `GET /api/templates`

```json
{
  "agents": [
    {
      "name": "GPT 5.5 Agent",
      "slug": "gpt-5.5-agent",
      "role": "Layout Architect",
      "latest_date": "2026-04-26",
      "template_url": "/templates/gpt-5.5-agent/latest.html",
      "raw_url": "https://raw.githubusercontent.com/maximoseo/webs-html-improvements-files/main/templates/gpt-5.5-agent/latest.html",
      "score": 92,
      "status": "Live",
      "history": [
        {"date": "2026-04-26", "score": 92, "status": "Live", "template_url": "/templates/gpt-5.5-agent/2026-04-26-template.html"}
      ]
    }
  ],
  "final": {
    "name": "Final Merged Template",
    "slug": "hermes-final",
    "role": "Hermes Combined Best-Of Output"
  }
}
```

Required dashboard features:
- live iframe preview
- raw HTML view
- copy HTML action
- date stamp
- agent name and role
- version history table
- final merged template card
- compare mode for any two templates
