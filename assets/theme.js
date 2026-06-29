/* ==========================================================================
   Lumina Theme - JS Core Architecture
   ========================================================================== */

// 1. Utilities & AJAX Handlers
// ==========================================================================
async function fetchCartData() {
  const res = await fetch(`${window.routes.cart_url}.js`);
  return res.json();
}

async function updateCartItemQuantity(key, quantity) {
  const response = await fetch(`${window.routes.cart_change_url}.js`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify({ id: key, quantity: parseInt(quantity) })
  });
  return response.json();
}

// 2. Custom Element: Cart Drawer
// ==========================================================================
class CartDrawer extends HTMLElement {
  constructor() {
    super();
    this.overlay = this.querySelector('.drawer__overlay');
    this.inner = this.querySelector('.drawer__inner');
    
    // Bind event handlers
    this.close = this.close.bind(this);
    this.open = this.open.bind(this);
    
    this.addEventListener('keyup', (evt) => {
      if (evt.code === 'Escape') this.close();
    });
  }

  connectedCallback() {
    this.initCartListeners();
  }

  initCartListeners() {
    // Intercept remove button clicks
    this.addEventListener('click', (event) => {
      if (event.target.classList.contains('cart-item__remove')) {
        event.preventDefault();
        const key = event.target.getAttribute('data-key');
        this.updateItemQuantity(key, 0);
      }
    });

    // Intercept quantity inputs
    this.querySelectorAll('quantity-input input').forEach(input => {
      input.addEventListener('change', (event) => {
        const key = event.target.getAttribute('data-key');
        const quantity = event.target.value;
        this.updateItemQuantity(key, quantity);
      });
    });
  }

  open() {
    this.setAttribute('aria-hidden', 'false');
    document.body.classList.add('overflow-hidden');
    this.inner.focus();
  }

  close() {
    this.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('overflow-hidden');
  }

  async updateItemQuantity(key, quantity) {
    try {
      this.classList.add('loading');
      const cart = await updateCartItemQuantity(key, quantity);
      
      // Update HTML parts dynamically by refreshing the drawer HTML
      await this.refreshDrawerHTML();
      
      // Update header cart count
      const headerCartCounter = document.querySelector('.cart-count-bubble span');
      if (headerCartCounter) {
        headerCartCounter.textContent = cart.item_count;
      }
      
      this.classList.remove('loading');
    } catch (error) {
      console.error('Error updating quantity:', error);
      this.classList.remove('loading');
    }
  }

  async refreshDrawerHTML() {
    // Fetch the current page content and extract the cart drawer elements
    const response = await fetch(window.location.href);
    const htmlText = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlText, 'text/html');
    
    const newItemsWrapper = doc.querySelector('#CartDrawer-Items');
    const oldItemsWrapper = this.querySelector('#CartDrawer-Items');
    if (newItemsWrapper && oldItemsWrapper) {
      oldItemsWrapper.innerHTML = newItemsWrapper.innerHTML;
    }

    const newFooter = doc.querySelector('.drawer__footer');
    const oldFooter = this.querySelector('.drawer__footer');
    if (newFooter && oldFooter) {
      oldFooter.innerHTML = newFooter.innerHTML;
    } else if (newFooter && !oldFooter) {
      // Add footer back if it was deleted due to empty cart
      const inner = this.querySelector('.drawer__inner');
      inner.appendChild(newFooter);
    } else if (!newFooter && oldFooter) {
      // Remove footer if cart is empty now
      oldFooter.remove();
    }

    // Toggle is-empty class on the drawer element
    if (doc.querySelector('#CartDrawer').classList.contains('is-empty')) {
      this.classList.add('is-empty');
    } else {
      this.classList.remove('is-empty');
    }

    // Reinitialize listeners for newly loaded elements
    this.initCartListeners();
  }
}
customElements.define('cart-drawer', CartDrawer);

// 3. Custom Element: Quantity Input
// ==========================================================================
class QuantityInput extends HTMLElement {
  constructor() {
    super();
    this.input = this.querySelector('input');
    this.changeEvent = new Event('change', { bubbles: true });

    this.querySelectorAll('button').forEach(
      (button) => button.addEventListener('click', this.onButtonClick.bind(this))
    );
  }

  onButtonClick(event) {
    event.preventDefault();
    const previousValue = this.input.value;

    if (event.target.name === 'plus') {
      this.input.stepUp();
    } else {
      this.input.stepDown();
    }

    if (previousValue !== this.input.value) {
      this.input.dispatchEvent(this.changeEvent);
    }
  }
}
customElements.define('quantity-input', QuantityInput);

// 4. Product Add-to-Cart Interceptor
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form[action="/cart/add"]');
  
  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const submitButton = form.querySelector('[type="submit"]');
      if (submitButton) submitButton.disabled = true;
      
      const formData = new FormData(form);
      
      try {
        const response = await fetch(`${window.routes.cart_add_url}.js`, {
          method: 'POST',
          headers: { 'Accept': 'application/json' },
          body: formData
        });
        
        if (!response.ok) throw new Error('Error adding item to cart');
        
        // Refresh the cart drawer content
        const cartDrawer = document.querySelector('cart-drawer');
        if (cartDrawer) {
          await cartDrawer.refreshDrawerHTML();
          cartDrawer.open();
        }
        
      } catch (error) {
        console.error(error);
        alert(window.cartStrings.error);
      } finally {
        if (submitButton) submitButton.disabled = false;
      }
    });
  });
  
  // Header scroll class toggle
  const headerWrapper = document.querySelector('.header-wrapper');
  if (headerWrapper) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        headerWrapper.classList.add('header-wrapper--scrolled');
      } else {
        headerWrapper.classList.remove('header-wrapper--scrolled');
      }
    });
  }
});
