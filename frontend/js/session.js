// session.js — Manejo de sesión local (sin backend ni IA)

document.addEventListener("DOMContentLoaded", () => {
    const navList = document.querySelector(".nav-list");
    const loginLink = navList.querySelector(".btn-login");

    // Verificar sesión
    const user = localStorage.getItem("userLogged");

    if (user && loginLink) {
        // Ocultar botón de login y mostrar logout
        loginLink.style.display = "none";

        const logoutBtn = document.createElement("button");
        logoutBtn.id = "logout-btn";
        logoutBtn.textContent = "Cerrar sesión";

        const li = document.createElement("li");
        li.appendChild(logoutBtn);
        navList.appendChild(li);

        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("userLogged");
            window.location.href = "index.html";
        });
    }
});
