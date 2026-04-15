# User Prompt — Deploy-to-n8n Button Request

**Date captured:** 2026-04-15 04:13 PT
**Session:** claude-code on `claude/html-improver-tab-ujRMs`
**Outcome:** shipped in commit `aeba6a9 feat(archives): Deploy-to-n8n button on workflow files`

## Prompt 1 (the ask)

> https://html-redesign-dashboard.maximo-seo.ai/ here i want to add option to apply the new design automaticly to n8n workflow (specific workflow for the domain) with a button (he will connect to n8n trhow th api) n8n api (webs): `<REDACTED — JWT-format n8n API key, pasted by user and now rotated>`
>
> https://websiseo.app.n8n.cloud/
>  if need to add this deploy n8n button just in the json files do it - think what will be the best

## Prompt 2 (approval)

> go

## Security note

The user's original message included a live n8n API key in JWT format. That
key has been stripped from this archival record because markdown files in
this repo are committed to a public GitHub repository. The working key is
only ever present in the Render service env var `N8N_WEBSISEO_API_KEY`
and must be rotated after being pasted into a chat transcript.
