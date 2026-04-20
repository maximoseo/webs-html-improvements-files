# RISK REPORT — 2026-04-20

## SECURITY RISKS

| Risk | Status | Mitigation |
|------|--------|------------|
| API keys in repo sources | ✅ CLEAR | No API keys found in any of 35 repos |
| Malicious code injection | ✅ CLEAR | Only README/markdown files read, no code executed |
| Token exposure in output | ✅ CLEAR | No tokens stored in any output file |

## TECHNICAL RISKS

| Risk | Level | Mitigation |
|------|-------|------------|
| CSS class conflicts with existing dta- prefix | LOW | All new modules use same dta- prefix — consistent, no conflict |
| Mega-skill too large for context window | MEDIUM | 1086 lines — use skills_tool:load + search, not full load |
| Module B3 email patterns differ from web patterns | LOW | Clearly marked as email-only, separate section |
| RTL Module 9 — Hebrew font availability | LOW | Uses system fallbacks (Arial), Google Fonts optional |
| CSS-only modal (Module 5) — checkbox hack accessibility | MEDIUM | Better to use JS in non-WP contexts; WP-safe tradeoff documented |
| AEO recommendations require site changes | LOW | Checklist only, no auto-implementation |

## COMPATIBILITY RISKS

| Risk | Level | Notes |
|------|-------|-------|
| `<details>/<summary>` in old WordPress | LOW | Supported since WP 5.0+ (2018) — safe |
| `clamp()` CSS function | LOW | Supported in all modern browsers (Chrome 79+, Firefox 75+, Safari 13.1+) |
| `backdrop-filter: blur()` | MEDIUM | Not supported in Firefox without flag pre-103 — add fallback `background: rgba()` |
| CSS `:focus-visible` | LOW | Supported Chrome 86+, Firefox 85+, Safari 15.4+ |
| `aspect-ratio` property | LOW | Chrome 88+, Firefox 89+, Safari 15+ |

## CONTENT RISKS

| Risk | Level | Notes |
|------|-------|-------|
| Placeholder content in templates | LOW | All templates use [BRACKETED_VARS] — clearly marked |
| Author box: real info required | MEDIUM | Must always replace [AUTHOR_NAME]/[AUTHOR_AVATAR] with real data |
| AEO token budget: <8000 tokens | LOW | Monitor article length — very long articles may exceed |

## RECOMMENDATIONS

1. For mega-skill usage: always use `skills_tool:search` first, then `skills_tool:load` — do not load full file blindly
2. For email HTML (Module B3): test in Litmus or Email on Acid before sending — Gmail/Outlook rendering differs significantly
3. For `backdrop-filter`: add explicit fallback: `background: rgba(0,0,0,0.8);` before the blur declaration
4. For Hebrew articles: verify Noto Sans Hebrew is loaded via Google Fonts or system font fallback is acceptable
