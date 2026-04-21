# SKILL: TuneLog — Self-Hosted Music Recommendation for Navidrome
**Source:** https://github.com/adiiverma40/tunelog
**Domain:** productivity
**Trigger:** Use when building personalized music playlists from listening behavior (skips/finishes/replays) on a Navidrome instance, or setting up a proxy layer to enhance Navidrome search results.

## Summary
TuneLog learns music taste by tracking interactions (skips, finishes, replays) on Navidrome without manual likes. Includes a proxy layer that improves search results with lyrics search and ranked results based on history. Docker or manual Python+Node setup.

## Key Patterns
- Tracks skips/finishes/replays → builds evolving playlists
- Optional proxy on port 4534 intercepts Navidrome requests to improve search
- Lyrics-based song search when songs have embedded lyrics
- Library auto-sync after Navidrome scans
- Docker Compose: backend API (8000) + frontend UI (5173)

## Usage
When user has a Navidrome instance and wants personalized playlists without manually rating songs.

## Code/Template
```bash
git clone https://github.com/adiiverma40/tunelog
cd tunelog
cp .env.example .env
# Edit .env: BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD, VITE_API_URL
docker compose up --build
# Web UI: http://localhost:5173
# Proxy: http://localhost:4534
```
