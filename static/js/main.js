/**
 * @fileoverview This is the main entry file to the js used for this project
 */

const eventHandler = (type, selectpr, callback, options) => {
  document.addEventListener(type, (e) => {
    if (e.target.matches(selectpr)) {
      callback(e);
    }
  }, options);
}

document.addEventListener('DOMContentLoaded', () => {
  // Sidebar
  eventHandler('click', '.menu-btn', () => {
    const sidebar = document.querySelector('.mobile-nav');

    if (sidebar.getBoundingClientRect().width === 0) {
      sidebar.style.width = '280px';
    } else {
      sidebar.style.width = '0px';
    }
  });
});

// Function to toggle side menu
function toggleMenu() {
  const sideMenu = document.querySelector('.mobile-nav');
  if (sideMenu.getBoundingClientRect().width == 0) {
    sideMenu.style.width = '300px';
  } else {
    sideMenu.style.width = '0px';
  }
}