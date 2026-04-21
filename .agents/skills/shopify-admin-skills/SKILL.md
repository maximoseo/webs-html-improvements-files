---
name: Shopify Admin Skills
source: https://github.com/40RTY-ai/shopify-admin-skills
category: Automation
purpose: 63 AI agent skills for operating Shopify stores via the Admin GraphQL API
when_to_use: When managing Shopify store operations including orders, inventory, pricing, customers, refunds, fulfillment, and marketing automation
tags: [shopify, ecommerce, automation, graphql, store-management]
---

# Shopify Admin Skills

## Purpose
63 skills across 10 categories that teach agents to operate Shopify stores with extended capabilities using the Admin GraphQL API. Covers the full store management lifecycle.

## When To Use
- Abandoned cart recovery and win-back campaigns
- Bulk price adjustments and inventory audits
- Order lookup, refunds, returns, address corrections
- Customer cohort analysis, B2B operations, duplicate finder
- Discount A/B testing, gift cards, conversion optimization
- Fulfillment ops: holds, routing, tracking, delivery SLA
- Finance: revenue reports, refund rates, AOV, tax, shipping
- Fraud risk detection, high-risk tagging, repeat purchase analysis
- Store management: redirects, drafts, discounts, pages

## How To Apply
1. Install via: `npx skills add 40RTY-ai/shopify-admin-skills`
2. Skills use dry_run: true for preview before execution
3. Each skill queries store, previews mutations, confirms, then reports
4. All mutations are reversible where possible; destructive ops require explicit confirmation

## Examples
- "Recover abandoned carts from last 7 days" → triggers abandoned-cart-recovery skill
- "Audit all products with inventory < 5 units" → triggers inventory-audit skill
- "Process refunds for orders flagged as fraud" → triggers fraud-risk + refund skills

## Integration Notes
- Requires Shopify Admin GraphQL API credentials (shop domain + access token via env var)
- Always preview with dry_run before mutations
- 10 categories: Marketing, Merchandising, Customer Support, Customer Ops, Conversion, Fulfillment, Finance, Order Intelligence, Returns, Store Management
