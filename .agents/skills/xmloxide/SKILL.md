# SKILL: xmloxide
**Source:** https://github.com/jonwiggins/xmloxide
**Domain:** code
**Trigger:** When needing a memory-safe, pure Rust XML/HTML parser as a drop-in replacement for libxml2

## Summary
xmloxide is a pure Rust reimplementation of libxml2 — the standard XML/HTML parsing library, which became unmaintained in Dec 2025. Passes 100% of W3C XML conformance tests (1727/1727) and all 8810 html5lib-tests. Zero unsafe in the public API.

## Key Patterns
- Arena-based DOM with `Document`, `NodeId`, `NodeKind`
- Multiple APIs: DOM tree, SAX2 streaming, XmlReader pull, push/incremental
- WHATWG HTML5 parser + SAX-like HTML5 streaming
- CSS selector engine (`css::select`) with `#id` fast lookup
- XPath 1.0+ evaluator with key XPath 2.0 functions
- DTD, RelaxNG, XSD, Schematron validation
- Optional serde XML serialization, async parsing (tokio)
- C/C++ FFI via `include/xmloxide.h`
- `xmllint` CLI: format, validate, xpath query, c14n

## Usage
```toml
[dependencies]
xmloxide = "0.x"
```

## Code/Template
```rust
use xmloxide::Document;
let doc = Document::parse_str("<root><child>Hello</child></root>").unwrap();
let root = doc.root_element().unwrap();
assert_eq!(doc.text_content(root), "Hello");

// CSS selectors
use xmloxide::css::select;
let results = select(&doc, root, "p.intro").unwrap();
```
