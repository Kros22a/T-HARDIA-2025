const API_URL = "https://t-hardia-2025-production.up.railway.app/api/v1";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");
    const messageDiv = document.getElementById("register-message");
    const btnText = document.querySelector(".btn-text");
    const btnLoading = document.querySelector(".btn-loading");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        btnText.style.display = "none";
        btnLoading.style.display = "inline-block";

        try {
            const res = await fetch(`${API_URL}/users/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || "Error al registrar usuario.");

            messageDiv.textContent = "✅ Registro exitoso. Redirigiendo al login...";
            messageDiv.style.color = "#4CAF50";

            setTimeout(() => {
                window.location.href = "login.html";
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
