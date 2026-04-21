# SKILL: chartli — Terminal Chart CLI
**Source:** https://github.com/ahmadawais/chartli
**Domain:** developer-tools
**Trigger:** Use when rendering charts in the terminal from numeric data, visualizing metrics in CI/CD pipelines, or generating SVG charts from text files.

## Summary
chartli is a CLI that renders terminal charts (ASCII, spark, bars, columns, heatmap, unicode, braille, SVG) from plain numeric text data or files. Zero config, works via npx, supports axis labels, series labels, and data label annotations.

## Key Patterns
- `npx chartli [file] -t <type>` where type: ascii, spark, bars, columns, heatmap, unicode, braille, svg
- `--first-column-x` treats first numeric column as x-axis labels
- `--x-axis-label`, `--y-axis-label`, `--series-labels`, `--x-labels` for annotations
- `--data-labels` shows raw values on chart
- Pipe stdin: `cat data.txt | npx chartli -t spark`
- Agent skill install: `npx skills add ahmadawais/chartli`

## Usage
When user wants to visualize numeric data in terminal, embed charts in CI output, or generate SVG charts from CSV/text files.

## Code/Template
```bash
npx chartli data.txt -t ascii -w 40 -h 10
npx chartli data.txt -t columns --first-column-x --series-labels sales,costs
npx chartli data.txt -t svg -m lines | sed -n '/^<?xml/,$p' > chart.svg

# Example data format
10 20 30 40 50
```
