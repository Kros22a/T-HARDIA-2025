// auth.js
// Manejo del estado de sesión, saludo dinámico del usuario y panel admin

document.addEventListener("DOMContentLoaded", () => {
    const loginNav = document.getElementById("login-nav");
    const logoutNav = document.getElementById("logout-nav");
    const logoutBtn = document.getElementById("logout-btn");
    const userGreeting = document.getElementById("user-greeting");
    const navList = document.querySelector(".nav-list");

    // Verificar si el usuario está logueado
    const isLoggedIn = localStorage.getItem("userLoggedIn") === "true";
    const authToken = localStorage.getItem("authToken");

    if (isLoggedIn && authToken) {
        const username = localStorage.getItem("username");
        const userEmail = localStorage.getItem("userEmail");
        const userRole = localStorage.getItem("userRole");
        const displayName = username || (userEmail ? userEmail.split("@")[0] : "Usuario");

        // Ocultar el botón de login y mostrar logout
        if (loginNav) loginNav.style.display = "none";
        if (logoutNav) logoutNav.style.display = "inline-block";

        // Mostrar saludo dinámico
        if (userGreeting) {
            userGreeting.style.display = "inline-block";
            userGreeting.textContent = `👋 Hola, ${displayName}`;
        }

        // Manejar elementos admin de forma ordenada
        if (navList) {
            // Remover elementos admin existentes para evitar duplicados
            const existingAdminItems = navList.querySelectorAll('[data-admin-item]');
            existingAdminItems.forEach(item => item.remove());

            // Insertar link admin si es admin
            if (userRole === "admin") {
                const adminLi = document.createElement('li');
                adminLi.setAttribute('data-admin-item', 'true');
                adminLi.innerHTML = `<a href="admin.html" class="nav-link" style="color: #ff6b6b; font-weight: bold; background: rgba(255,107,107,0.1); padding: 5px 10px; border-radius: 5px; margin: 0 5px;">
                    <i class="fas fa-crown"></i> Admin Panel
                </a>`;
                
                // Insertar antes del logout-nav para mantener el orden
                if (logoutNav) {
                    navList.insertBefore(adminLi, logoutNav);
                } else {
                    navList.appendChild(adminLi);
                }
            }
        }

    } else {
        // Usuario no logueado
        if (loginNav) loginNav.style.display = "inline-block";
        if (logoutNav) logoutNav.style.display = "none";
        if (userGreeting) userGreeting.style.display = "none";
        
        // Remover elementos admin si existen
        if (navList) {
            const adminItems = navList.querySelectorAll('[data-admin-item]');
            adminItems.forEach(item => item.remove());
        }
    }

    // Función de cierre de sesión (solo una vez)
    if (logoutBtn && !logoutBtn.hasAttribute('data-auth-initialized')) {
        logoutBtn.setAttribute('data-auth-initialized', 'true');
        logoutBtn.addEventListener("click", () => {
            // Borrar todos los datos guardados
            localStorage.removeItem("userLoggedIn");
            localStorage.removeItem("authToken");
            localStorage.removeItem("userEmail");
            localStorage.removeItem("userId");
            localStorage.removeItem("username");
            localStorage.removeItem("userRole");

            // Restaurar la navegación
            if (loginNav) loginNav.style.display = "inline-block";
            if (logoutNav) logoutNav.style.display = "none";
            if (userGreeting) userGreeting.style.display = "none";

            // Remover elementos admin
            if (navList) {
                const adminItems = navList.querySelectorAll('[data-admin-item]');
                adminItems.forEach(item => item.remove());
            }

            // Redirigir al inicio
            window.location.href = "index.html";
        });
    }
});
