<!-- Demoted from skill: html-redesign-dashboard-hardening; original path: domain/html-redesign-dashboard-hardening -->

---
name: html-redesign-dashboard-hardening
description: Audit and harden the HTML Redesign Dashboard single-file SPA — tokens, a11y, CLS, Lighthouse, mobile compact header, git push via PowerShell, Obsidian sync.
triggers:
  - "audit dashboard"
  - "harden dashboard"
  - "lighthouse dashboard"
  - "a11y dashboard"
  - "redesign dashboard"
  - "mobile header"
  - "CLS fix"
---

# HTML Redesign Dashboard Hardening

## Context
- Source: `/mnt/c/Users/seoadmin/webs-html-improvements-files-clean/index.html`
- Repo: `maximoseo/webs-html-improvements-files` (Render auto-deploys on push)
- Live URL: https://html-redesign-dashboard.maximo-seo.ai/
- Obsidian vault sync path: `C:\Obsidian\HTML REDESIGN\HTML REDESIGN\HTML REDESIGN\dashboard\`
- Single-file SPA (~7,200–8,400 lines), no build toolchain — all patches are additive in-place edits

## MANDATORY after EVERY change (3-item checklist)
1. **git push via PowerShell** (WSL git times out on HTTPS push):
   ```bash
   powershell.exe -Command "\$pat=(Get-Content 'C:\\Users\\seoadmin\\.hermes\\secure\\github_pat_full.txt' -Raw).Trim(); cd 'C:\\Users\\seoadmin\\webs-html-improvements-files-clean'; git remote set-url origin \"https://\$pat@github.com/maximoseo/webs-html-improvements-files.git\"; git pull --rebase origin main; git push origin main; git remote set-url origin 'https://github.com/maximoseo/webs-html-improvements-files.git'; git log --oneline -3"
   ```
   PAT file: `C:\Users\seoadmin\.hermes\secure\github_pat_full.txt` — must contain the **full 40-char PAT** on a single line, no trailing whitespace.
   > ⚠️ `github_pats.txt` stores a **truncated** value — do **not** use it. Write the full PAT once to `github_pat_full.txt` with:
   > `echo -n 'ghp_XXXX...' > /mnt/c/Users/seoadmin/.hermes/secure/github_pat_full.txt`
   Always restore clean URL after push (already included in the command above).
2. **Obsidian sync** — copy `index.html`, `server.py`, `n8n-workflow-map.json` to vault path above (direct filesystem write from WSL via `/mnt/c/`).
3. **Live verify** — HTTP 200 + spot-check changed DOM nodes on the live URL after Render redeploy (~40s).

## Baseline Lighthouse scores (2026-04-20, commit 772c27b)
| Category | Score |
|---|---:|
| Performance | 96 |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 100 |
**CWV:** LCP 1.5s ✓, CLS 0.098 ✓, TBT 110ms ✓, TTI 1.9s ✓

## Phase history
| Commit | Phase | Key changes |
|---|---|---|
| 52f5fab | 1.0 | Token scale, skip link, `<main>`, focus-visible, modal aria-labels, role=progressbar + aria-live, microcopy |
| 3480027 | 1.5 | `.page-header` / `.metadata-strip` / `.action-bar` primitives, container queries, Esc coverage |
| 3a61249 | 2.0 | Tab a11y (role=tablist + aria-selected), meta description, initial CLS reservation |
| 0a17d3c | 2.1 | Heading-order fix, broader CLS reservation |
| 239c9e3 | 2.2 | body padding-top tuned → CLS 0.283 → 0.098 |
| 772c27b | 2.3 | Mobile sticky header compact to 55px (was ~200px) |

## Common audit steps
1. Run Lighthouse headless (mobile + desktop):
   ```bash
   lighthouse https://html-redesign-dashboard.maximo-seo.ai/ \
     --output=json --output=html \
     --form-factor=mobile --emulated-form-factor=mobile \
     --chrome-flags="--headless --no-sandbox" \
     --output-path=/tmp/lh-mobile
   ```
2. Check DOM for a11y gaps:
   - `grep -c 'aria-label' index.html` — should be ≥15
   - `grep -c 'role="progressbar"' index.html` — should be ≥2
   - `grep -c 'aria-live' index.html` — should be ≥1
   - `grep -c '<main' index.html` — should be 1
   - `grep -c 'skip' index.html` — should be ≥3
3. Mobile header height — simulate via iframe at 390px viewport and screenshot

## Refract integration for redesign work
- When the user asks for redesign directions, UI variants, mobile-header alternatives, microcopy options, naming, or non-obvious UX solutions, also load `refract` before proposing the final answer.
- Use `refract` during divergent ideation so you consider multiple valid UI directions before converging on one recommendation.
- Keep `refract` scoped to creative/solution-space exploration. Do **not** use it for factual verification, lighthouse checks, deployment verification, auth diagnostics, or other tasks where a single grounded answer is required.
- Good fit examples in this dashboard: mobile header simplification options, CTA wording, card layout alternatives, filter UX variants, empty-state copy, and ways to reduce repetitive "glassmorphism" defaults.

## CLS root causes (known)
- Mobile header wrapping → body padding-top mismatch → fixed by matching `padding-top` fallbacks to real measured height
- Stats grid late hydration → fixed by reserving `min-height` on `.stats-grid` before JS runs
- Always reserve space for dynamically-rendered grids before JS hydration

## Deferred (separate workstreams)
- React/router migration (needs build toolchain)
- Sidebar nav restructure (needs design pass)
- Playwright matrix
- CSS/JS minification (needs build step)
- Component-library extraction

## Pitfalls
- WSL git push via HTTPS times out — always use PowerShell
- If the main working copy has many unrelated uncommitted changes, do NOT patch/push from it. Create a clean deployment worktree from `origin/main`/`HEAD`, apply only the scoped patch there, validate, commit, and push from that clean worktree. This prevents clobbering user edits.
- Always `git fetch` / `git pull --rebase origin main` before final push. If remote `main` advanced and rebase causes conflicts in `index.html`, abort/reset the clean deploy worktree and reapply the minimal patch on top of the latest `origin/main`; never force-push or overwrite newer dashboard work.
- Dashboard API routes are auth-protected. Local smoke tests for new `/api/...` endpoints must login first via `/api/auth/login` and reuse the `dash_auth` cookie; otherwise 401 is expected and not a route failure.
- Some environments may not have `pytest`; still run `python3 -m py_compile server.py`, parse `index.html` with `html.parser`, run `node --check` on extracted JS snippets, boot the local server on an unused `PORT`, and smoke `/api/health` plus authenticated endpoint calls.
- Lighthouse mobile CLS is sensitive to header height mismatches on first paint — always set `body { padding-top }` in CSS before JS runs
- `role="progressbar"` alone does not announce updates — always pair with a `role="status" aria-live="polite"` companion element
- Tab `aria-selected` must be updated in the JS `showPage()` function, not just in HTML
- Single-file SPA — validate HTML with Python `html.parser` after every patch to catch unclosed tags
