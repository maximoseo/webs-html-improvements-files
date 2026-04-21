# SKILL: Boneyard
**Source:** https://github.com/0xGF/boneyard
**Domain:** design
**Trigger:** When adding skeleton loading screens to any React, Vue, Svelte, Angular, or React Native app

## Summary
Pixel-perfect skeleton loading screens auto-generated from your real UI, with no manual measurement. A CLI/Vite plugin snapshots element layouts at multiple breakpoints and generates `.bones.json` files consumed by `<Skeleton>` wrappers.

## Key Patterns
- **Zero config capture**: CLI opens headless browser, finds every `<Skeleton name="...">`, snapshots layout at multiple breakpoints (375, 768, 1280 default)
- **Cross-framework**: Works with React, Preact, Vue, Svelte 5, Angular, React Native with identical `.bones.json` output
- **Vite plugin**: `boneyardPlugin()` in vite.config.ts auto-captures on dev server start and re-captures on HMR
- **Animation options**: `'pulse'` (default), `'shimmer'`, `'solid'`; stagger delay between bones; fade transition on load end
- **Dark mode**: Separate `darkColor` prop (default: `rgba(255,255,255,0.06)`) vs light `color` (default: `rgba(0,0,0,0.08)`)
- **React Native**: Dynamic Type support — bones scale to user's accessibility text size setting

## Usage
```bash
npm install boneyard-js
npx boneyard-js build          # capture once
npx boneyard-js build --watch  # re-capture on HMR
```
Import registry in app entry: `import './bones/registry'`

Then wrap content: `<Skeleton name="blog-card" loading={isLoading}><BlogCard /></Skeleton>`

Config file `boneyard.config.json` for global defaults.

## Code/Template
```tsx
// React
import { Skeleton } from 'boneyard-js/react'
function Page() {
  const { data, isLoading } = useFetch('/api/post')
  return (
    <Skeleton name="blog-card" loading={isLoading} animate="shimmer" stagger={80} transition={300}>
      {data && <BlogCard data={data} />}
    </Skeleton>
  )
}
```
```ts
// vite.config.ts
import { boneyardPlugin } from 'boneyard-js/vite'
export default defineConfig({ plugins: [boneyardPlugin()] })
```
