# SKILL: App Store Preflight — iOS/macOS Pre-Submission Checker
**Source:** https://github.com/truongduy2611/app-store-preflight-skills
**Domain:** marketing
**Trigger:** Use before submitting an iOS or macOS app to the App Store to catch common rejection reasons including metadata violations, privacy issues, subscription compliance, and app-type specific requirements.

## Summary
An AI agent skill that runs pre-submission checks on Xcode projects against 100+ Apple Review Guidelines, organized by app type (subscriptions, social/UGC, kids, health, games, macOS, AI apps, crypto/finance, VPN). Integrates with `asc` CLI for metadata inspection.

## Key Patterns
- 10 app-type checklists: all_apps, subscription_iap, social_ugc, kids, health_fitness, games, macos, ai_apps, crypto_finance, vpn
- Catches: competitor terms in metadata, Apple trademark misuse, missing ToS/Privacy Policy, misleading pricing, data collection without disclosure
- Process: identify app type → pull metadata (`asc metadata pull`) → scan rules → report with severity → autofix + re-validate
- Install: `npx skills add truongduy2611/app-store-preflight-skills`
- Requires `asc` CLI: `brew install asc`

## Usage
Run before every App Store submission. Specify app type to load the correct checklist. Review severity-sorted findings and apply fixes before submitting.

## Code/Template
```bash
npx skills add truongduy2611/app-store-preflight-skills
brew install asc

# Pull metadata
asc metadata pull --app "MyApp" --version "1.0" --dir ./metadata

# Agent will scan against rules in references/rules/
# Categories: metadata/, subscription/, privacy/, ui_ux/, code/
```
