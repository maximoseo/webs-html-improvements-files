# SKILL: Posterskill (Academic Poster Generator)
**Source:** https://github.com/ethanweber/posterskill
**Domain:** design
**Trigger:** When creating academic conference posters, research posters, or scientific presentation posters

## Summary
An agent skill for generating high-quality academic conference posters from research content. Takes paper text, figures, and metadata and produces professionally designed poster layouts suitable for academic venues.

## Key Patterns
- **Academic poster conventions**: Title/authors/affiliation header, abstract, methods, results, conclusion panels
- **Research figure integration**: Proper captioning, spacing, figure-text relationship
- **Multiple layout options**: Portrait A0/A1, landscape variants, multi-column grids
- **Typography**: Clear hierarchy — title (large), section headers, body text, captions
- **Color schemes**: Institutional colors, clean academic palettes, high contrast for readability
- **QR codes**: Auto-generated links to paper/code/demo

## Usage
Provide paper content (abstract, methods, results, figures) → agent generates a structured HTML/PDF poster.

Common poster dimensions: A0 (841×1189mm portrait), A1, or 36×48in for US venues.

## Code/Template
```html
<!-- Academic poster layout template -->
<div class="poster" style="width:841mm;height:1189mm;font-family:'Open Sans',sans-serif">
  <!-- Header -->
  <header style="background:#003366;color:#fff;padding:40px;text-align:center">
    <h1 style="font-size:56px;margin:0">Paper Title: A Study of Something Important</h1>
    <p style="font-size:28px;margin-top:12px">Author One¹, Author Two², Author Three¹</p>
    <p style="font-size:22px">¹University A  ²University B</p>
  </header>

  <!-- 3-column body -->
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;padding:32px">
    <section>
      <h2>Abstract</h2>
      <p>We present...</p>
    </section>
    <section>
      <h2>Methods</h2>
      <figure><img src="method.png" /><figcaption>Fig 1: Architecture</figcaption></figure>
    </section>
    <section>
      <h2>Results</h2>
      <table><!-- comparison table --></table>
    </section>
  </div>

  <!-- Footer with QR codes -->
  <footer style="display:flex;justify-content:space-around;padding:24px">
    <div>📄 Paper: <img src="qr-paper.svg" width="80" /></div>
    <div>💻 Code: <img src="qr-code.svg" width="80" /></div>
  </footer>
</div>
```
