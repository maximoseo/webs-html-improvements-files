# SKILL: element-source — DOM Element to Source File Mapping
**Source:** https://github.com/aidenybai/element-source
**Domain:** code
**Trigger:** When an AI agent needs to map a DOM element to its source file location (React, Vue, Svelte, Solid, Preact)

## Summary
Library that resolves any DOM element to its source file path, line number, component name, and full component stack. Works with React, Preact, Vue, Svelte, Solid. Powers "click element → give source to AI agent" workflows.

## Key Patterns
- resolveElementInfo(element) → { tagName, componentName, source, stack }
- resolveSource, resolveStack, resolveComponentName as focused APIs
- createSourceResolver with custom framework resolvers (svelteResolver, vueResolver)
- formatStackFrame / formatStack for human-readable output

## Usage
Use in browser devtools extensions or agent tools that need source context from UI elements.

## Code/Template
```typescript
import { resolveElementInfo, resolveSource, resolveStack } from "element-source";

const info = await resolveElementInfo(document.querySelector("#root button"));
// { tagName: "button", componentName: "Counter",
//   source: { filePath: "src/Counter.tsx", lineNumber: 12, columnNumber: 5 },
//   stack: [...] }

// Preact: import "preact/debug" in development first
// Custom resolvers:
import { createSourceResolver, svelteResolver, vueResolver } from "element-source";
const { resolveElementInfo } = createSourceResolver({ resolvers: [svelteResolver, vueResolver] });
```
