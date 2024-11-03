/**
 * @fileoverview This is the main entry file to the js used for this project
 */


document.addEventListener('DOMContentLoaded', () => {
  // Sidebar
  eventHandler('click', '.menu-btn', () => {
    toggleSideMenu();
  });

  // Toasts
  eventHandler('click', '.btn', () => {
    closeToast();
  });
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

const closeToast = () => {
  document.querySelector('.toast').style.display = 'none';
}