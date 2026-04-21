# SKILL: hucre — Zero-Dependency Spreadsheet Engine
**Source:** https://github.com/productdevbook/hucre
**Domain:** developer-tools
**Trigger:** Use when reading or writing XLSX, CSV, or ODS files in TypeScript/JavaScript with zero dependencies, streaming support, schema validation, or edge runtime compatibility.

## Summary
hucre is a pure TypeScript, zero-dependency spreadsheet engine supporting XLSX, CSV, and ODS read/write with streaming, schema validation, round-trip preservation, conditional formatting, sparklines, tables, and images. Works in Edge/browser/Node, native ESM.

## Key Patterns
- `readXlsx(buffer)` → `workbook.sheets[0].rows`
- `writeXlsx({ sheets: [{ name, columns, data }] })` → Buffer
- Tree-shakeable: `import { readXlsx } from "hucre/xlsx"` (~14KB gzipped)
- `parseCsv` / `writeCsv` for CSV (~2KB gzipped)
- Streaming read/write for large files
- No eval, CSP compliant, works in Cloudflare Workers

## Usage
When user needs XLSX/CSV manipulation in TypeScript without SheetJS/ExcelJS dependencies, especially in Edge runtimes or with strict CSP policies.

## Code/Template
```typescript
import { readXlsx, writeXlsx } from "hucre";

const workbook = await readXlsx(buffer);
console.log(workbook.sheets[0].rows);

const xlsx = await writeXlsx({
  sheets: [{
    name: "Products",
    columns: [
      { header: "Name", key: "name", width: 25 },
      { header: "Price", key: "price", width: 12, numFmt: "$#,##0.00" },
    ],
    data: [{ name: "Widget", price: 9.99 }],
  }],
});
```
