
    document.addEventListener("DOMContentLoaded", function () {
        let elements = document.querySelectorAll(".fade-in");
        let observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                }
            });
        }, { threshold: 1.0 });

        elements.forEach(el => observer.observe(el));
    });
