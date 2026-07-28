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

const appsTable = document.querySelector("#apps_table tbody");

function setAppsStatus(message) {
    if (!appsTable) return;
    appsTable.innerHTML = "";
    const row = document.createElement("tr");
    row.className = "apps_status_row";
    const cell = document.createElement("td");
    cell.colSpan = 2;
    cell.textContent = message;
    row.appendChild(cell);
    appsTable.appendChild(row);
}

if (appsTable) {
    fetch("/download/apps/manifest.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`manifest request failed: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const apps = Object.keys(data);

            if (apps.length === 0) {
                setAppsStatus("no apps available yet");
                return;
            }

            appsTable.innerHTML = "";

            apps.forEach(app => {
                let row = document.createElement("tr");

                let name = document.createElement("td");
                name.textContent = app;

                let download = document.createElement("td");

                let button = document.createElement("a");
                button.textContent = "download";
                button.href = "/download/apps/" + app;
                button.download = app;

                download.appendChild(button);

                row.appendChild(name);
                row.appendChild(download);

                appsTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Failed to load apps:", error);
            setAppsStatus("couldn't load apps — try again later");
        });
}