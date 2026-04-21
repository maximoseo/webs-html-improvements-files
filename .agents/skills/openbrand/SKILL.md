# SKILL: OpenBrand
**Source:** https://github.com/ethanjyx/OpenBrand
**Domain:** design
**Trigger:** When extracting brand assets (logos, colors, fonts, design guidelines) from any company/website

## Summary
An API and tool for automatically extracting brand assets from any website — logos, color palettes, typography, and design guidelines. Enables programmatic brand asset discovery for design systems, competitor analysis, or design token generation.

## Key Patterns
- **Brand asset extraction**: Logos (SVG/PNG), primary/secondary colors, font families, spacing patterns
- **Automated discovery**: Crawls target URL, finds and extracts brand-relevant CSS and visual assets
- **Structured output**: Returns normalized JSON with brand identity components
- **Use cases**: Design system seeding, competitive brand analysis, automatic DESIGN.md generation

## Usage
Point at any company URL → receive structured brand data including color palette, logo URLs, typography, and key design properties.

## Code/Template
```python
from openbrand import BrandExtractor

extractor = BrandExtractor()
brand = extractor.extract("https://stripe.com")

print(brand.colors.primary)    # '#635BFF'
print(brand.logo.svg_url)      # 'https://stripe.com/img/logo.svg'
print(brand.typography.primary)  # 'Sohne, system-ui'
print(brand.name)              # 'Stripe'

# Export as design tokens
tokens = brand.to_design_tokens()
# Export as Tailwind config
tailwind = brand.to_tailwind_config()
# Export as DESIGN.md
design_md = brand.to_design_md()
```
