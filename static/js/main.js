/**
 * @fileoverview This is the main entry file for the JavaScript used in this project.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Sidebar
  eventHandler('click', '.menu-btn', toggleSideMenu);

  // Toasts
  eventHandler('click', '.toast-close', closeToast);
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
    toast.style.display = 'none';
  } else {
    console.error('Toast element not found');
  }
};
