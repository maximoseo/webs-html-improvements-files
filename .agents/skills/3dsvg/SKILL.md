# SKILL: 3DSVG (SVG to 3D Interactive)
**Source:** https://github.com/renatoworks/3dsvg
**Domain:** design
**Trigger:** When creating 3D interactive text/logo, turning SVGs into 3D objects, or embedding 3D design elements in web apps

## Summary
The easiest way to turn SVGs into interactive 3D. A React component `<SVG3D>` extrudes any SVG/text into a 3D object with 10 material presets, 7 animations, configurable lighting, and exports to PNG/MP4/GLB/STL/OBJ. Includes a visual editor at 3dsvg.design.

## Key Patterns
- **Simple API**: `<SVG3D text="Hello" animate="spin" />` or `<SVG3D svg="/logo.svg" material="gold" />`
- **10 material presets**: Default, Plastic, Metal, Glass, Rubber, Chrome, Gold, Clay, Emissive, Holographic
- **7 animations**: Spin, Float, Pulse, Wobble, Swing, Spin+Float, or static
- **4 input methods**: Text (10 Google Fonts), Pixel Editor, SVG Code, File Upload
- **Lighting controls**: Key light position/intensity, ambient intensity, shadows
- **Export formats**: PNG (transparent/background, up to 4K), MP4/WebM video (60fps), GLB, STL, OBJ, PLY
- **Responsive**: Auto-zooms on portrait/narrow viewports
- **Interactive**: Drag rotation with momentum, scroll zoom, cursor-follow orbit
- **Embed code**: Copy-ready JSX snippet from editor state
- **Tech**: React Three Fiber + Three.js + Next.js + Tailwind v4 + opentype.js + FFmpeg WASM

## Usage
```bash
npm install 3dsvg
```

Embed in any React app with the `<SVG3D>` component. Use the web editor at 3dsvg.design for visual configuration.

## Code/Template
```tsx
import { SVG3D } from "3dsvg";

// Text-based 3D
<SVG3D text="Hello" animate="spin" material="chrome" />

// SVG logo 3D
<SVG3D svg="/logo.svg" material="gold" animate="float" />

// Full configuration
<SVG3D
  text="Brand"
  animate="spin"
  material="glass"
  lighting={{ keyIntensity: 1.5, ambientIntensity: 0.3, shadows: true }}
  camera={{ zoom: 1.2, autoOrbit: true }}
  style={{ width: "100%", height: "400px" }}
/>
```

Materials reference:
```
default | plastic | metal | glass | rubber | chrome | gold | clay | emissive | holographic
```
Animations reference:
```
spin | float | pulse | wobble | swing | spin-float | none
```
