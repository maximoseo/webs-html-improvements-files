# SKILL: Terraink - Custom City Map Poster Generator
**Source:** https://github.com/yousifamanuel/terraink
**Domain:** code
**Trigger:** When building open-source map visualization tools, creating print-ready poster generation from OpenStreetMap data, or implementing MapLibre-based web apps

## Summary
Open-source web app for creating custom city map posters from real OpenStreetMap data. Features smart geocoding, curated themes, detailed map layers (roads, water, parks, buildings), typography controls, and high-resolution PNG export. Built with React + MapLibre + Bun/Vite.

## Key Patterns
- MapLibre for client-side map rendering with OpenMapTiles/OpenFreeMap tile hosting
- Nominatim geocoding for city/region search or coordinate input
- Configurable map layers: roads, water bodies, parks, building footprints with per-layer styling
- Google Fonts integration for typography
- High-resolution PNG export for print-ready output

## Usage
```bash
bun install && bun run dev
# Check .env.example for optional environment variables
```

## Code/Template
Stack: React + TypeScript + Vite + Bun + MapLibre + OpenStreetMap + Cloudflare + Docker
Data: OpenStreetMap contributors → OpenMapTiles → OpenFreeMap (tile hosting) → MapLibre (render)
