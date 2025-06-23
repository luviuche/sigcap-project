// app/static/script.js

// Nos aseguramos de que el script se ejecute solo cuando todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- Lógica para el Formulario de la Fachada (Reserva Completa) ---
    const facadeForm = document.getElementById('facade-form');
    facadeForm.addEventListener('submit', async (event) => {
        // Prevenimos que el formulario recargue la página (comportamiento por defecto)
        event.preventDefault();

        // Recogemos los datos de los inputs del formulario
        const email = document.getElementById('facade-email').value;
        const password = document.getElementById('facade-password').value;
        const profesionalId = document.getElementById('facade-prof-id').value;

        // Creamos el cuerpo de la petición JSON como lo espera nuestra API
        const requestBody = {
            usuario: {
                email: email,
                password: password
            },
            cita: {
                profesional_id: parseInt(profesionalId)
            }
        };

        // Hacemos la llamada a la API usando fetch()
        try {
            const response = await fetch('/reservas-completas', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            const result = await response.json();
            displayResponse(result, response.status);

        } catch (error) {
            displayResponse({ error: 'Error de red o conexión' }, 500);
        }
    });

    // --- Lógica para el Formulario del Decorador (Calcular Costo) ---
    const decoratorForm = document.getElementById('decorator-form');
    decoratorForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const citaId = document.getElementById('decorator-cita-id').value;
        const conUrgencia = document.getElementById('decorator-urgencia').checked;
        const conImpuesto = document.getElementById('decorator-impuesto').checked;

        // Construimos la URL dinámicamente con los parámetros
        let url = `/citas/${citaId}/costo-detallado?`;
        const params = [];
        if (conUrgencia) {
            params.push('urgencia=true');
        }
        if (conImpuesto) {
            params.push('impuesto=true');
        }
        url += params.join('&');

        // Hacemos la llamada GET
        try {
            const response = await fetch(url);
            const result = await response.json();
            displayResponse(result, response.status);
        } catch (error) {
            displayResponse({ error: 'Error de red o conexión' }, 500);
        }
    });

    // --- Lógica para el Botón de Deshacer (Command) ---
    const undoButton = document.getElementById('undo-button');
    undoButton.addEventListener('click', async () => {
        // Hacemos la llamada a nuestro endpoint de deshacer
        try {
            const response = await fetch('/acciones/deshacer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
                // No necesita cuerpo (body)
            });

            const result = await response.json();
            displayResponse(result, response.status);

        } catch (error) {
            displayResponse({ error: 'Error de red o conexión' }, 500);
        }
    });

    // --- Función de ayuda para mostrar la respuesta en la página ---
    function displayResponse(data, status) {
        const responseArea = document.getElementById('response-area');
        // Usamos JSON.stringify con formato para que se vea bonito
        responseArea.innerHTML = `<strong>Estado: ${status}</strong>\n\n${JSON.stringify(data, null, 2)}`;

        // Cambiamos el color del borde si hay un error
        if (status >= 400) {
            responseArea.style.borderColor = 'red';
            responseArea.style.color = 'red';
        } else {
            responseArea.style.borderColor = '#4CAF50'; // Borde verde para éxito
            responseArea.style.color = 'black';
        }
    }
});