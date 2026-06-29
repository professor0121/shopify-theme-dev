# Shopify Theme Development Guidelines

This document defines coding standards, architecture, and quality rules for developing custom Shopify Online Store 2.0 themes.

## 1. Directory Structure
A standard Shopify theme must follow this directory structure:
- `assets/` - Static assets (CSS, JS, images, fonts). Use modular files.
- `config/` - Settings schema definition (`settings_schema.json`) and data presets (`settings_data.json`).
- `layout/` - Primary layouts (e.g., `theme.liquid`).
- `locales/` - Translation files (e.g., `en.default.json`).
- `sections/` - Reusable, customizable sections with Liquid schemas.
- `snippets/` - Reusable Liquid markup chunks / components.
- `templates/` - JSON configurations for pages (e.g., `index.json`, `product.json`).

## 2. Liquid Standards & Performance
- **Image Optimization**: Always specify widths and use the `image_url` filter with `image_tag` or `srcset`. Use `loading: 'lazy'` for below-the-fold images.
  ```liquid
  {{ product.featured_media | image_url: width: 600 | image_tag: loading: 'lazy', alt: product.title }}
  ```
- **Conditional Loading**: Do not bundle everything in a single massive CSS file if styles are section-specific. Use inline `<style>` inside sections or dynamic `<link>` elements.
- **Minimize Loops**: Avoid nesting `{% for %}` loops inside each other. Retrieve resources directly by handle where possible.
- **Escape Outputs**: Always use appropriate filters like `| escape`, `| json`, or `| asset_url` to prevent rendering issues and secure output data.

## 3. CSS Architecture
- **Design Tokens**: Define theme-wide tokens using CSS custom properties (variables) on the `:root` level, mapped from `settings.settings_schema`.
- **Naming Convention**: Use BEM (Block, Element, Modifier) styling conventions to prevent collisions (e.g., `.header__logo--active`).
- **Responsive Layout**: Build mobile-first. Use CSS Grid and Flexbox for modern layouts. Avoid hardcoded heights and widths.
- **Glassmorphism Style**: For premium aesthetics, use backdrop filters with subtle borders:
  ```css
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  ```

## 4. JS & Web Components
- **Custom Elements**: Wrap dynamic UI patterns in HTML5 Custom Elements to capsule logic:
  ```javascript
  class CartDrawer extends HTMLElement {
    constructor() {
      super();
      // Initialize events
    }
  }
  customElements.define('cart-drawer', CartDrawer);
  ```
- **Vanilla ES6**: Avoid jQuery. Use `fetch` API for AJAX operations, `querySelectorAll`, and arrow functions.
- **State Synchronization**: Use CustomEvents to coordinate states between different sections (e.g., updating header cart counter when product is added).

## 5. Accessibility (a11y)
- **Keyboard Navigation**: Ensure all interactive elements (buttons, inputs, links, drawer toggles) are focusable and support keyboard interaction (e.g., closing drawers on ESC).
- **Aria Roles**: Use `aria-expanded`, `aria-hidden`, and `aria-controls` for toggleable components.
- **Skip Links**: Include skip-to-content links for screen readers.

## 6. Theme Validation
- Always run `shopify theme check` to ensure correctness before building/deploying.
- Every section schema must specify valid inputs and default settings.
