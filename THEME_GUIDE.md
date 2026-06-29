# Lumina Theme – Merchant & Developer Documentation

Welcome to **Lumina**, a high-converting, performance-oriented Shopify Online Store 2.0 theme. Lumina is designed from the ground up to offer sleek glassmorphic aesthetics, instant AJAX navigation, custom modular sections, and accessible user flows.

---

## 1. Directory Structure

Lumina follows Shopify's modern theme structure for maximum compatibility:

```text
├── assets/             # Core Stylesheets (theme.css) and ES6 Scripts (theme.js)
├── config/             # Theme settings schema (settings_schema.json) and presets (settings_data.json)
├── layout/             # Master layout files (theme.liquid)
├── locales/            # Translation/Internationalization definitions (en.default.json)
├── sections/           # Reusable blocks and full-width customizable page sections
├── snippets/           # Reusable HTML snippets and SVGs (product-card.liquid, icons)
└── templates/          # OS 2.0 JSON layout configuration definitions (index.json, product.json, etc.)
```

---

## 2. Getting Started (Development Setup)

To run or customize the Lumina theme locally on your machine, follow these steps:

### Prerequisites
- Node.js installed (v18+)
- Shopify CLI installed globally:
  ```bash
  npm install -g @shopify/cli @shopify/theme
  ```

### Step 1: Initialize Local Theme Development Server
Open your terminal in the theme project directory and run:
```bash
shopify theme dev
```
*You will be prompted to log in to your Shopify partner account and select a store to preview.*

### Step 2: Open Theme Editor
Once the CLI starts successfully, it will provide three links:
1. **Local Preview**: `http://127.0.0.1:9292` (live reloads on local edits).
2. **Shopify Theme Editor**: Link to customize sections dynamically.
3. **Preview Link**: Shareable preview link.

---

## 3. Customize Colors & Typography

Lumina makes full use of Shopify's theme editor config schema:

### Design Tokens
Customizations in the Theme Editor automatically map to CSS custom variables in `:root` inside `theme.liquid`:
* `--color-bg`: Main background color (Default: `#0f0f11` - Charcoal Dark).
* `--color-text`: Primary text color (Default: `#f3f4f6`).
* `--color-primary`: Accent color 1 (Indigo).
* `--color-secondary`: Accent color 2 (Purple).
* `--grid-spacing`: Custom grid margins for spacing control.

To adjust settings, open the **Theme Editor** -> **Theme Settings** tab.

---

## 4. Section Customizations

Lumina is an **Online Store 2.0** theme. This means every page is built using modular JSON layouts, allowing you to drag-and-drop sections anywhere on any page.

### Included Sections:
1. **Header**: Sticky glassmorphic bar. Supports custom logo upload, mobile hamburger drawer, and inline search.
2. **Hero Banner**: Full-width impact banner with dynamic parallax overlay, dual CTAs, and title animation.
3. **Featured Collection**: Showcases selected collections in a clean, interactive product card grid. Includes hover scale effects and "View All" redirects.
4. **Main Product Details**: Custom page layout containing product media gallery, quantity elements, dynamic price updates when option-radios are clicked, and tab-based accordion menus.
5. **Main Collection Grid**: Collection listing with sorting, layout grids, and standard pagination buttons.
6. **Footer**: Custom multi-column brand text, newsletter sign-ups, quick-link navigation, and social icon networks.

---

## 5. JavaScript Architecture & Cart Drawer

Lumina avoids heavy libraries like jQuery in favor of clean, performant **Web Components (Custom Elements)**.

### Component: `<cart-drawer>`
Manages the state and markup of the slide-out cart panel.
* **Opening**: Calling `document.querySelector('cart-drawer').open()` will transition the panel onto the screen and set `aria-hidden="false"`.
* **Closing**: Triggers when clicking the overlay, the close 'X' button, or hitting the `Escape` key.
* **AJAX Operations**:
  - Intercepts add-to-cart form submissions globally.
  - Submits forms asynchronously via `fetch` to `/cart/add.js`.
  - Re-renders cart content dynamically using DOM parsing, without refreshing the page.

### Component: `<quantity-input>`
Manages quantity incrementing and decrementing.
* Updates state and fires `change` events that prompt the parent `<cart-drawer>` to update Shopify's `/cart/change.js` API dynamically.

---

## 6. Accessibility (a11y) & Performance Guidelines

### Keyboard Focus Management
The AJAX cart drawer traps keyboard focus while active. When opened, focus shifts to the close button, and tab actions loop within the drawer. Pressing `ESC` closes the drawer immediately and returns focus to the trigger button.

### Optimizing Images
Images are rendered using liquid markup responsive width filters:
```liquid
{{ product.featured_media | image_url: width: 533 | image_tag: loading: 'lazy' }}
```
* **`loading="lazy"`**: Standardizes deferred loading of below-the-fold elements for faster initial page loads.
* **`width`**: Defines optimized dimensions, avoiding heavy asset payloads.
