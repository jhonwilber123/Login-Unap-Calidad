// static/js/navbar.js

document.addEventListener('DOMContentLoaded', function () {
    const navbarToggle = document.querySelector('.navbar-toggler');
    const navbarNav = document.getElementById('navbarSupportedContent');

    navbarToggle.addEventListener('click', function () {
        navbarNav.classList.toggle('active');
    });

    // Manejar la expansión de dropdown en móviles
    const dropdownToggles = document.querySelectorAll('.nav-item.dropdown > .nav-link');

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            if (window.innerWidth <= 768) { // Solo en móviles
                e.preventDefault(); // Evita que el enlace navegue
                const parent = this.parentElement;
                parent.classList.toggle('active');
            }
        });
    });

    // **Nuevas Funcionalidades para PC**

    // 1. Dropdown en hover para pantallas grandes
    const dropdowns = document.querySelectorAll('.nav-item.dropdown');

    dropdowns.forEach(function (dropdown) {
        dropdown.addEventListener('mouseenter', function () {
            if (window.innerWidth > 768) { // Solo en pantallas grandes
                const dropdownMenu = this.querySelector('.dropdown-menu');
                dropdownMenu.classList.add('show');
                this.classList.add('show');
            }
        });

        dropdown.addEventListener('mouseleave', function () {
            if (window.innerWidth > 768) { // Solo en pantallas grandes
                const dropdownMenu = this.querySelector('.dropdown-menu');
                dropdownMenu.classList.remove('show');
                this.classList.remove('show');
            }
        });
    });

    // 2. Cambiar estilo de la navbar al hacer scroll (Sticky Navbar)
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});
