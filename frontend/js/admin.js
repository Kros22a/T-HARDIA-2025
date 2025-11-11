// Panel administrativo admin.js
const API_URL = "https://t-hardia-2025-production.up.railway.app/api/v1";

document.addEventListener('DOMContentLoaded', function() {
    loadAdminData();
});

async function loadAdminData() {
    try {
        // Cargar estadísticas
        await loadStats();
        
        // Cargar usuarios
        await loadUsers();
        
        // Cargar comparaciones
        await loadComparisons();
        
        // Cargar respuestas de encuestas
        await loadSurveyResponses();
        
    } catch (error) {
        console.error('Error loading admin data:', error);
    }
}

async function loadStats() {
    try {
        const authToken = localStorage.getItem('authToken');
        
        // Cargar usuarios
        const usersResponse = await fetch(`${API_URL}/users/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const users = await usersResponse.json();
        document.getElementById('users-count').textContent = users.length;
        
        // Cargar comparaciones
        const comparisonsResponse = await fetch(`${API_URL}/comparisons/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const comparisons = await comparisonsResponse.json();
        document.getElementById('comparisons-count').textContent = comparisons.length;
        
        // Cargar respuestas de encuestas
        const surveysResponse = await fetch(`${API_URL}/surveys/responses`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const surveys = await surveysResponse.json();
        document.getElementById('surveys-count').textContent = surveys.length;
        
        // Cargar posts de blog
        const blogResponse = await fetch(`${API_URL}/blog/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const blogPosts = await blogResponse.json();
        document.getElementById('blog-count').textContent = blogPosts.length;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadUsers() {
    try {
        const authToken = localStorage.getItem('authToken');
        
        const response = await fetch(`${API_URL}/users/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const users = await response.json();
        
        const usersList = document.getElementById('users-list');
        let html = '<div class="users-grid">';
        
        users.forEach(user => {
            html += `
                <div class="user-card">
                    <h4>${user.username}</h4>
                    <p>Email: ${user.email}</p>
                    <p>Registrado: ${new Date(user.created_at).toLocaleDateString()}</p>
                    <p>Último login: ${user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Nunca'}</p>
                    <p>Admin: ${user.is_admin ? 'Sí' : 'No'}</p>
                </div>
            `;
        });
        
        html += '</div>';
        usersList.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading users:', error);
        document.getElementById('users-list').innerHTML = '<p>Error al cargar usuarios</p>';
    }
}

async function loadComparisons() {
    try {
        const authToken = localStorage.getItem('authToken');
        
        const response = await fetch(`${API_URL}/comparisons/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const comparisons = await response.json();
        
        const comparisonsList = document.getElementById('comparisons-list');
        let html = '<div class="comparisons-list">';
        
        comparisons.slice(0, 10).forEach(comp => {
            html += `
                <div class="comparison-item">
                    <h4>${comp.component1} vs ${comp.component2}</h4>
                    <p>Usuario: ${comp.user_id}</p>
                    <p>Fecha: ${new Date(comp.created_at).toLocaleDateString()}</p>
                    <p>Generado por IA: ${comp.ai_generated ? 'Sí' : 'No'}</p>
                </div>
            `;
        });
        
        html += '</div>';
        comparisonsList.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading comparisons:', error);
        document.getElementById('comparisons-list').innerHTML = '<p>Error al cargar comparaciones</p>';
    }
}

// Nueva función para cargar preguntas
async function loadQuestions() {
    try {
        const authToken = localStorage.getItem('authToken');
        const response = await fetch(`${API_URL}/surveys/questions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const questions = await response.json();
        // Crea un mapa ID -> texto (ej. {1: "¿Prefieres CPUs Intel o AMD?", ...})
        const questionMap = {};
        questions.forEach(q => {
            questionMap[q.id] = q.question;  // Usa q.question para el texto
        });
        return questionMap;
    } catch (error) {
        console.error('Error loading questions:', error);
        return {};  // Retorna vacío si falla
    }
}

async function loadSurveyResponses() {
    try {
        const authToken = localStorage.getItem('authToken');
        
        // Carga las preguntas primero
        const questionMap = await loadQuestions();
        
        const response = await fetch(`${API_URL}/surveys/responses`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const responses = await response.json();
        
        const responsesList = document.getElementById('survey-responses');
        let html = '<div class="responses-list">';
        
        responses.slice(0, 10).forEach(resp => {
            const questionText = questionMap[resp.question_id] || `Pregunta ID: ${resp.question_id}`;  // Fallback si no encuentra
            html += `
                <div class="response-item">
                    <p><strong>Pregunta:</strong> ${questionText}</p>
                    <p><strong>Usuario:</strong> ${resp.user_id}</p>
                    <p><strong>Respuesta:</strong> ${resp.response ? 'Sí' : 'No'}</p>
                    <p><strong>Fecha:</strong> ${new Date(resp.created_at).toLocaleDateString()}</p>
                </div>
            `;
        });
        
        html += '</div>';
        responsesList.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading survey responses:', error);
        document.getElementById('survey-responses').innerHTML = '<p>Error al cargar respuestas</p>';
    }
}
