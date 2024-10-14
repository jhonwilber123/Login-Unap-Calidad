// static/js/navbar.js

document.addEventListener('DOMContentLoaded', function () {
    const navbarToggle = document.getElementById('navbarToggle');
    const navbarNav = document.getElementById('navbarNav');

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
});
