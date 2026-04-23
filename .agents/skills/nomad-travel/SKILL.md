# SKILL: NOMAD (TREK) — Self-Hosted Collaborative Travel Planner
**Source:** https://github.com/mauriceboe/NOMAD
**Domain:** productivity
**Trigger:** Use when building or deploying a self-hosted travel planning app with collaborative real-time editing, interactive maps, budget tracking, packing lists, and PDF export.

## Summary
TREK/NOMAD is a self-hosted collaborative travel planner (Vue + FastAPI + WebSocket) with drag-and-drop day planning, Leaflet maps, Google Places/OSM search, budget tracking, multi-currency support, packing lists, reservations, document management, PDF export, and PWA/offline support.

## Key Patterns
- Real-time sync via WebSocket — changes appear instantly across all users
- Leaflet interactive map with photo markers, clustering, route optimization
- Budget: category expenses, pie chart, per-person/per-day splitting, multi-currency
- Packing: category checklists, user assignment, templates, weight tracking (optional)
- PWA: offline service worker, install on iOS/Android, Workbox caching
- Admin-toggleable features: bag tracking weight, packing templates
- Docker deployment via `docker pull mauriceboe/trek`

## Usage
When user needs a self-hosted travel planning tool for trips, group travel, or remote team offsites with shared itinerary editing.

## Code/Template
```bash
docker pull mauriceboe/trek
docker compose up -d
# Demo: https://demo-nomad.pakulat.org

# Stacks: Vue frontend + FastAPI backend + WebSocket + SQLite
```
