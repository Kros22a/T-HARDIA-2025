const API_URL = "https://t-hardia-2025-production.up.railway.app/api/v1";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const messageDiv = document.getElementById("login-message");
    const btnText = document.querySelector(".btn-text");
    const btnLoading = document.querySelector(".btn-loading");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        btnText.style.display = "none";
        btnLoading.style.display = "inline-block";

        try {
            // Paso 1: Login para obtener token
            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);

            const res = await fetch(`${API_URL}/users/login`, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formData,
            });

            const loginData = await res.json();

            if (!res.ok) throw new Error(loginData.detail || "Error al iniciar sesión.");

            // Paso 2: Obtener datos del usuario usando el token
            const userRes = await fetch(`${API_URL}/users/me?token=${loginData.access_token}`);

            const userData = await userRes.json();

            if (!userRes.ok) throw new Error("Error al obtener datos del usuario.");

            // Guardar todos los datos en localStorage
            localStorage.setItem("userLoggedIn", "true");
            localStorage.setItem("authToken", loginData.access_token);
            localStorage.setItem("userEmail", userData.email);
            localStorage.setItem("userId", userData.id);
            localStorage.setItem("username", userData.username || userData.email.split('@')[0]);
            
            // Verificar si es admin
            const isAdmin = userData.is_admin || 
                          userData.role === "admin" || 
                          userData.is_superuser || 
                          email.includes("admin") ||
                          email === "admin@t-hardia.com"; // AJUSTA ESTE EMAIL
            
            if (isAdmin) {
                localStorage.setItem("userRole", "admin");
            }

            messageDiv.textContent = "✅ Inicio de sesión exitoso. Redirigiendo...";
            messageDiv.style.color = "#4CAF50";

            // 🔹 Redirigir según el rol
            setTimeout(() => {
                if (isAdmin) {
                    window.location.href = "admin.html";
                } else {
                    window.location.href = "index.html";
                }
            }, 1500);
        } catch (err) {
            messageDiv.textContent = "❌ " + err.message;
            messageDiv.style.color = "#f44336";
        } finally {
            btnText.style.display = "inline";
            btnLoading.style.display = "none";
        }
    });
});
