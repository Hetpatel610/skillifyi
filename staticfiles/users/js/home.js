const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');

navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active'); // Toggle the 'active' class to show/hide the menu
});
document.getElementById('menu-icon').addEventListener('click', function() {
  document.getElementById('nav-links').classList.toggle('active');
});
