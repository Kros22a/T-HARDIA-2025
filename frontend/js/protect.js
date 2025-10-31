// protect.js — Bloquea el acceso a páginas sin sesión activa

document.addEventListener("DOMContentLoaded", () => {
    // Obtenemos los datos del usuario guardados en el login
    const isLoggedIn = localStorage.getItem("userLoggedIn") === "true";
    const authToken = localStorage.getItem("authToken");
    const userEmail = localStorage.getItem("userEmail");

    // Si no hay sesión activa, redirigir al login
    if (!isLoggedIn || !authToken || !userEmail) {
        alert("⚠️ Debes iniciar sesión para acceder a esta página.");
        window.location.href = "login.html";
        return;
    }

    // Si hay sesión activa, opcional: mostrar el usuario en consola
    console.log(`🔐 Usuario autenticado: ${userEmail}`);
    
    // Opcional: Verificar que el token no haya expirado
    // (esto es más avanzado y depende de tu implementación de JWT)
});
