/**
 * @fileoverview Main entry point for the application.
 * @package
 * @version 1.0.0
 * @since 1.0.0
 * @module main
 * 
 */

window.addEventListener('scroll', function() {
  var header = document.querySelector('.header-container');
  var scrollPosition = window.scrollY;

  if (scrollPosition > 0) {
    header.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
  } else {
    header.style.backgroundColor = 'transparent';
  }
});