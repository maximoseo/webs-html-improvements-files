---
created: 2026-03-26T11:46:03.939Z
title: Audit responsive app and deploy
area: general
files:
  - package.json
---

## Problem

The app at `https://maximo-seo.ai/app` needs a full responsive audit, remediation pass, verification cycle, and deployment. The future work should identify the actual frontend stack and CSS approach from the local codebase, run the app locally, review the UI across mobile, tablet, desktop, and ultra-wide breakpoints, document every layout and interaction defect, and fix them without changing branding unless an accessibility issue requires it. The task also requires accessibility-aware mobile behavior, RTL checks if Hebrew content exists, Lighthouse validation with strong scores, a clean production build, production-build smoke testing, GitHub push, Render deployment verification, and a final implementation summary. Manual Render deployment may require `RENDER_API_KEY` and `RENDER_SERVICE_ID`.

## Solution

Follow the five-phase workflow captured in the prompt:

1. Discovery and audit: inspect `package.json` and project files to determine the stack, start the local dev server, collect screenshots at 320, 375, 414, 768, 1024, 1280, 1440, 1920, and 2560 widths, and log all responsive and interaction issues by severity.
2. Fixes: apply mobile-first responsive corrections using modern layout techniques, fluid sizing, accessible mobile navigation, responsive tables, mobile-friendly forms, robust image handling, and logical properties for RTL where needed.
3. Verification: retest all listed breakpoints and key interactions, run Lighthouse for performance, accessibility, best practices, and SEO, fix critical findings, and ensure there are no console errors.
4. Pre-deploy checks: run the production build, serve the built output locally, verify the built app matches the dev server, and confirm all pages still work.
5. Deploy and report: create a clean fix commit, push to `main`, verify Render deployment, confirm the live site reflects the fixes, and report issue counts, Lighthouse deltas, changed files, commit hash, deploy status, and any remaining manual follow-ups.
