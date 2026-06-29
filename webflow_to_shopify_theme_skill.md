---
name: antigravity
description: Converts an exported Webflow site (HTML/CSS/JS pages in a "pages" folder) into a fully customizable Shopify Liquid theme with zero UI breaks. Use this whenever the user mentions converting Webflow to Shopify, porting a Webflow export into a theme, turning static HTML/CSS pages into Liquid templates/sections, or wants a Shopify theme built from existing pixel-perfect Webflow markup. Always trigger when a "pages" folder of exported Webflow HTML is referenced alongside Shopify.
---

# Antigravity — Webflow → Shopify Theme Converter

Converts exported Webflow pages into a production-grade, fully customizable Shopify Online Store 2.0 theme, preserving the original UI exactly (pixel parity — "no UI breaks") while making every section/block schema-driven.

## Non-negotiable rules

1. **Zero UI breaks.** Visual output must match the Webflow export pixel-for-pixel at every breakpoint Webflow generated (desktop/tablet/mobile/landscape). Never "improve" or restructure layout unless asked.
2. **Fully customizable.** Every visually distinct block (hero, nav, footer, cards, CTA, testimonials, etc.) becomes a Shopify **section** with a `{% schema %}` exposing text, images, colors, links, and repeatable blocks via the theme editor. No hardcoded copy/images in section files — pull from schema settings with sensible defaults matching the original Webflow content.
3. **CSS: prefer my own, but UI wins.** Default to rewriting Webflow's generated CSS into a clean, deduped, BEM-ish or utility stylesheet under `assets/`. BUT if any rewrite risks behavior/visual drift (complex Webflow interactions, custom animations, flex/grid quirks), keep the original Webflow CSS for that component verbatim instead of risking a break. Never sacrifice fidelity for cleanliness.
4. Preserve all Webflow JS interactions (sliders, accordions, animations, IX2 triggers, lightboxes) — port to `assets/*.js` and load via `{% javascript %}` or layout scripts. Re-test that triggers/classes still match after Liquid templating.

## Workflow

### Step 1 — Inventory the Webflow export
- `view`/`bash_tool` into the uploaded `pages` folder. List every `.html` page, the shared `css/`, `js/`, `images/`/`fonts/` folders.
- Identify shared chrome (nav, footer) vs page-unique content by diffing the `<header>`/`<nav>`/`<footer>` markup across pages.
- Note all Webflow-specific cruft to strip: `data-w-id`, `wf-...` classes that are purely Webflow's loader (KEEP layout-relevant `w-` classes if CSS depends on them, just confirm), Webflow's own `webflow.js` runtime (replace functionality with vanilla JS), and the `<!-- Last Published -->` comment block.

### Step 2 — Scaffold the theme
Standard Online Store 2.0 structure:
```
theme/
├── layout/theme.liquid
├── templates/ (index.json, page.*.json, product.json, collection.json, 404.json, etc.)
├── sections/ (one per distinct Webflow block: header, footer, hero, ...)
├── snippets/ (reusable bits: icon-svg, price, card-product, etc.)
├── assets/ (app.css, app.js, fonts, images — copied verbatim from Webflow export)
├── config/settings_schema.json + settings_data.json
└── locales/en.default.json
```

### Step 3 — Convert chrome first
- Header/Nav and Footer → `sections/header.liquid`, `sections/footer.liquid`, included via `layout/theme.liquid`. These must render on every page identically to Webflow.
- Add them to `{% schema %}` with logo, menu, social links, colors as settings so they're editable.

### Step 4 — Convert each unique page
For each Webflow page:
- Map static page → Shopify template (`page.about.json`, `index.json` for home, `product.json`/`collection.json` if it's a PDP/PLP layout, otherwise a generic `page.{handle}.json`).
- Break the page body into ordered sections matching Webflow's visual blocks 1:1 (don't merge/split blocks the original didn't have).
- Each section: copy the exact HTML structure and classes from the Webflow export into the `.liquid` file, replace static text/images/links with `{{ section.settings.x }}` / blocks loop, keep all original class names so the ported CSS still applies untouched.
- Wire dynamic Shopify data only where it's actually a product/collection page (e.g. swap a Webflow "product card" mockup for real `{{ product.title }}`, `{{ product.featured_image }}`, etc.) — never invent dynamic data on purely static marketing pages.

### Step 5 — CSS
- Concatenate/dedupe Webflow CSS into `assets/base.css` (resets, typography, grid/flex utilities Webflow generated) + one file per section if it's large, e.g. `assets/section-hero.css`, loaded only where used via `{{ 'section-hero.css' | asset_url | stylesheet_tag }}` in that section file (keeps unused CSS off other pages).
- Re-map Webflow's auto-generated breakpoints (`@media (max-width: 991px/767px/479px)`) 1:1 — these are Webflow's actual breakpoints, don't guess new ones.
- If asked for "preferred" CSS architecture and no fidelity risk: convert to CSS custom properties for colors/spacing (driven by `settings_data.json` theme settings) so merchants can recolor in the editor without touching code.

### Step 6 — Verify no UI break
- Open each converted template's rendered HTML mentally against the Webflow source: same DOM nesting, same classes, same image dimensions/alt text, same link hrefs.
- Confirm responsive behavior: same flex/grid wrap points, same hidden/show classes at each breakpoint.
- Confirm JS interactions still fire (check class/id selectors weren't renamed during Liquid-ification).
- Run `theme check` (Shopify CLI) if available to catch Liquid syntax errors before handing off.

### Step 7 — Deliver
- Zip the theme folder, or note it's ready for `shopify theme push` / "Upload theme" in Shopify admin.
- List, page by page, which Webflow page mapped to which Shopify template+sections, and which settings were exposed for customization — so the user can sanity-check fidelity and editability at a glance.

## When something can't be 1:1
If a Webflow interaction/CMS feature has no Shopify equivalent (e.g. Webflow CMS collection list vs Shopify collections/metafields), flag it explicitly rather than silently approximating, and propose the closest Shopify-native pattern (metafields, Shopify CMS-equivalent via collections/blog, or a manually maintained block list) — always asking before substituting structure that could change behavior.

## Reference
See `/mnt/skills/user/shopify-developer/SKILL.md` for deeper Liquid/section/schema/Theme Check conventions — consult it for syntax details while executing this workflow.