# SKILL: Grimmory
**Source:** https://github.com/grimmory-tools/grimmory
**Domain:** code
**Trigger:** When setting up a self-hosted book library manager with reading progress sync, multi-device support, and AI metadata enrichment

## Summary
A self-hosted book collection manager (successor to BookLore) with a built-in reader for PDF/EPUB/comics, OPDS support, Kobo/KOReader sync, multi-user accounts, and BookDrop for auto-import of watched folders.

## Key Patterns
- Docker Compose deployment (MariaDB + grimmory containers)
- BookDrop: drop files into watched folder → auto-detect, enrich metadata, queue for import
- Metadata from Google Books, Open Library, Amazon (editable)
- Supported formats: EPUB, MOBI, AZW/AZW3, FB2, PDF, CBZ/CBR/CB7, M4B/M4A/MP3 (audiobooks)
- Multi-user: separate shelves, progress, OIDC or local auth
- OPDS for compatible apps; Kobo + KOReader sync
- Smart Shelves: rule-based filtering, tagging, full-text search
- One-click sharing to Kindle or email
- Helm chart + Podman Quadlet deployment options
- Stable images tagged `vX.Y.Z` + `latest`; nightly from `develop` tagged `nightly`

## Usage
Create `.env` file, use provided docker-compose.yml, run `docker compose up -d`. Open http://localhost:6060. Migrating from BookLore: keep service name/ports/volumes, update only the image line.

## Code/Template
```yaml
# docker-compose.yml snippet
services:
  grimmory:
    image: grimmory/grimmory:latest
    ports: ["6060:6060"]
    volumes:
      - ./data:/app/data
      - ./books:/books
      - ./bookdrop:/bookdrop
    environment:
      - DATABASE_URL=jdbc:mariadb://mariadb:3306/grimmory

# .env
APP_USER_ID=1000
DATABASE_URL=jdbc:mariadb://mariadb:3306/grimmory
DB_PASSWORD=ChangeMe_2025!
```
