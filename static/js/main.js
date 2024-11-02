/**
 * @fileoverview This is the main entry file to the js used for this project
 */


document.addEventListener('DOMContentLoaded', () => {
  // Sidebar
  eventHandler('click', '.menu-btn', () => {
    toggleSideMenu();
  });

  // Get the class names from the config file
  formatElements();
});

const eventHandler = (type, selectpr, callback, options) => {
  document.addEventListener(type, (e) => {
    if (e.target.matches(selectpr)) {
      callback(e);
    }
  }, options);
}

const toggleSideMenu = () => {
  const sidebar = document.querySelector('.mobile-nav');

    if (sidebar.getBoundingClientRect().width === 0) {
      sidebar.style.width = '280px';
    } else {
      sidebar.style.width = '0px';
    }
}
