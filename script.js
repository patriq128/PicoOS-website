// nav toggle (mobile)
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav_links");

if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });

    navLinks.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => navLinks.classList.remove("active"));
    });
}

const panels = document.querySelectorAll(".panel");

if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    panels.forEach((panel) => observer.observe(panel));
} else {
    panels.forEach((panel) => panel.classList.add("visible"));
}