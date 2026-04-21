# SKILL: DuckDB-HNSW-ACORN
**Source:** https://github.com/cigrainger/duckdb-hnsw-acorn
**Domain:** code
**Trigger:** When doing filtered vector similarity search in DuckDB, especially when WHERE clauses return too few results or memory is a concern

## Summary
A DuckDB extension fork that fixes filtered HNSW search using the ACORN-1 algorithm and adds RaBitQ binary quantization (21-30x compression). WHERE clauses are pushed into HNSW graph traversal for correct k results.

## Key Patterns
- ACORN-1 pushes filter predicates into HNSW traversal (not post-filter)
- Selectivity-based strategy: >60% standard HNSW, 1-60% ACORN-1, <1% brute-force
- RaBitQ: `WITH (quantization = 'rabitq')` — 21x memory reduction at 128 dims
- Metadata join pattern: JOIN metadata on BIGINT key → optimizer runs filtered HNSW
- Per-group top-K: `GROUP BY category` + `min_by(id, distance, k)`
- Configurable thresholds: `SET hnsw_acorn_threshold`, `SET hnsw_bruteforce_threshold`
- `PRAGMA hnsw_compact_index('idx')` to reclaim space after deletes

## Usage
Install as DuckDB extension. Use standard SQL — optimizer auto-detects filter/join patterns. Create indexes with `CREATE INDEX ... USING HNSW (vec) WITH (metric='cosine', quantization='rabitq')`.

## Code/Template
```sql
-- Standard filtered search (returns exactly 10 results)
SELECT * FROM items
WHERE category = 'X'
ORDER BY array_distance(vec, [1,2,3]::FLOAT[3])
LIMIT 10;

-- RaBitQ for large dims (saves 21x+ memory)
CREATE INDEX idx ON items USING HNSW (vec) WITH (quantization = 'rabitq');
SET hnsw_rabitq_oversample = 10;  -- higher = better recall

-- Per-group nearest neighbors
SELECT category, min_by(id, array_distance(vec, query_vec), 5)
FROM items GROUP BY category;
```
