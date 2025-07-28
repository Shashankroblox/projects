'use strict';





document.addEventListener("DOMContentLoaded", function () {
  const navToggler = document.querySelector("[data-nav-toggler]");
  const navbar = document.querySelector("[data-navbar]");

  if (navToggler && navbar) {
    navToggler.addEventListener("click", function () {
      navbar.classList.toggle("active");
      navToggler.classList.toggle("active");
    });
  }
});

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("active");
}

