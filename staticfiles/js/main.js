/**
 * @fileoverview This is the main entry file for the JavaScript used in this project.
 * It handles events for sidebar toggling, toast notifications, and product menu display.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Attach event listeners for various UI interactions
  eventHandler('click', '.menu-btn', toggleSideMenu); // Sidebar toggle
  eventHandler('click', '.toast-close', closeToast);  // Close toast notifications
  eventHandler('click', '.filter-btn', toggleProductsMenu); // Toggle product filter menu
});

/**
 * Event handler function to attach event listeners to elements matching the given selector.
 * @param {string} type - The type of event (e.g., 'click').
 * @param {string} selector - The CSS selector for the target elements.
 * @param {Function} callback - The function to be executed when the event is triggered.
 * @param {Object} [options] - Optional event listener options.
 */
const eventHandler = (type, selector, callback, options) => {
  document.addEventListener(type, (e) => {
    if (e.target.matches(selector)) {
      callback(e);
    }
  }, options);
};

/**
 * Toggles the visibility of the sidebar menu.
 * If the sidebar is currently hidden, it will be shown; otherwise, it will be hidden.
 */
const toggleSideMenu = () => {
  const sidebar = document.querySelector('.mobile-nav');
  if (sidebar) {
    // Toggle sidebar width between 280px and 0px
    sidebar.style.width = sidebar.getBoundingClientRect().width === 0 ? '280px' : '0px';
  } else {
    console.error('Sidebar element not found');
  }
};

/**
 * Closes the toast notification by setting its display style to 'none'.
 */
const closeToast = () => {
  const toast = document.querySelector('.toast');
  if (toast) {
    // Hide toast notification
    toast.style.display = 'none';
  } else {
    console.error('Toast element not found');
  }
};

/**
 * Toggles the height of the products menu.
 * If the menu is currently hidden, it will be shown; otherwise, it will be hidden.
 */
const toggleProductsMenu = () => {
  const productsMenu = document.querySelector('.products-mobile-menu');
  if (productsMenu) {
    // Toggle products menu height between 450px and 0px
    productsMenu.style.height = productsMenu.getBoundingClientRect().height === 0 ? '450px' : '0px';
  } else {
    console.error('Products menu element not found');
  }
};
