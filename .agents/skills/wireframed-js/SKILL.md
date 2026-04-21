# SKILL: Wireframed.js (3D Wireframe Generator)
**Source:** https://github.com/Lywald/Wireframed.js
**Domain:** design
**Trigger:** When generating 3D wireframe art, node-graph visual processing, procedural 3D aesthetics from models

## Summary
A visual node-graph engine built in the browser with Three.js for generating stunning wireframe art from any 3D model. Think Houdini/Blender geometry nodes but browser-native with zero install. Load GLTF/GLB/OBJ/FBX, chain 30+ processing nodes, export presets as JSON.

## Key Patterns
- **No install**: Open `index.html` — no npm, no bundler, no server required (or use optional Node/Python server)
- **Node-graph pipeline**: Directed graph re-evaluates automatically on changes; drag-and-drop nodes with real-time preview
- **30+ processing nodes** across 6 categories (geometry, wireframe, color, transform, effects, composite)
- **Deep Randomize**: Swaps to a new graph topology from 20 curated layouts + randomizes all parameters — one click, infinite aesthetics
- **Embeddable runtime**: `wireframed-runtime.js` embeds any saved preset into a Three.js project in ~15 lines
- **Export**: Save/load graph as compact JSON preset
- **Supported formats**: GLTF, GLB, OBJ, FBX

## Usage
Open `index.html` directly in browser (via a local server for file imports).
1. Load Model via top bar
2. Drag nodes from left panel → connect ports
3. Select node → edit parameters in right panel
4. Save Preset → `.json` file

Windows: double-click `launch.bat`; macOS/Linux: `./launch.sh`

## Code/Template
```ts
// Embed a saved preset in your Three.js project
import { WireframedRuntime } from './wireframed-runtime.js';

const runtime = new WireframedRuntime({
  preset: '/my-preset.json',
  container: document.getElementById('canvas-container'),
  width: 800,
  height: 600
});
runtime.start();
```

```json
{
  "nodes": [
    { "id": "load", "type": "ModelLoader", "params": { "file": "model.glb" } },
    { "id": "wire", "type": "WireframeExtract", "params": { "threshold": 0.5 } },
    { "id": "color", "type": "ColorRamp", "params": { "colors": ["#00f", "#0ff"] } }
  ],
  "edges": [["load", "wire"], ["wire", "color"]]
}
```
