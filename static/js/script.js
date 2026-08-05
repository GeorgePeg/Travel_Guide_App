document.addEventListener('DOMContentLoaded', function() {
    //Toggle Menu
    const navbarNav = document.getElementById('navbarNav');
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler && navbarNav) {
        navbarToggler.addEventListener('click', function () {
            navbarNav.classList.toggle('show');
        });
    }
    const navLinks = document.querySelectorAll('a[href^="#"]');
    const menuCollapse = document.getElementById('navbarNav');
    const bsCollapse = menuCollapse ? new bootstrap.Collapse(menuCollapse, {toggle: false}):null;
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            // Κλείσιμο του Menu των κινητών
            if (bsCollapse && menuCollapse.classList.contains('show')) {
                bsCollapse.hide();
            }
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start'});
                }
            }
        });
    });
});