let toastTimeout;

function copyToClipboard(text) {
    if (!navigator.clipboard) {
        console.error('Clipboard API no soportada');
        return;
    }

    navigator.clipboard.writeText(text)
        .then(() => showToast('Copiado al portapapeles'))
        .catch(err => {
            console.error('Error al copiar:', err);
            showToast('No se pudo copiar', 'error');
        });
}

function showToast(message, type = 'success') {
    let toast = document.getElementById('copy-toast');

    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'copy-toast';

        Object.assign(toast.style, {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            minWidth: '220px',
            padding: '12px 18px',
            borderRadius: '8px',
            color: '#fff',
            fontFamily: 'system-ui, sans-serif',
            fontSize: '14px',
            fontWeight: '500',
            boxShadow: '0 4px 12px rgba(0,0,0,.15)',
            zIndex: '9999',
            opacity: '0',
            transform: 'translateY(20px)',
            transition: 'all .3s ease'
        });

        document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.style.backgroundColor =
        type === 'success' ? '#198754' : '#dc3545';

    clearTimeout(toastTimeout);

    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    toastTimeout = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
    }, 2500);
}

function abrirModalFormPlataforma(data = {}) {
    const modal = document.getElementById('modalPlataforma');
    const form = document.getElementById('formPlataforma');
    const title = document.getElementById('modalTitle');
    const btn = document.getElementById('btnGuardar');

    // Elementos del logo
    const previewContainer = document.getElementById('form_logo_preview_container');
    const logoPreview = document.getElementById('p_logo_preview');
    const fileInput = document.getElementById('form_url_logo');

    // Limpiamos el formulario por si acaso
    form.reset();

    if (data.id) {
        // MODO EDICIÓN
        title.innerHTML = '<i class="bi bi-pencil-square"></i> Editar Plataforma';
        btn.textContent = 'Actualizar Plataforma';
        
        // Rellenamos los campos
        document.getElementById('form_plataforma_id').value = data.id;
        document.getElementById('form_nombre').value = data.nombre;
        document.getElementById('form_precio_total').value = data.precio;
        document.getElementById('form_dia_cobro').value = data.dia;
        document.getElementById('form_cuota').value = data.cuota;
        document.getElementById('form_correo_admin').value = data.correo;

        // --- MANEJO DE LA IMAGEN EN EDICIÓN ---
        if (data.logo) {
            logoPreview.src = `/static/uploads/${data.logo}`;
            previewContainer.style.display = 'block'; // Mostramos la previsualización
        } else {
            previewContainer.style.display = 'none';
        }

        // Siempre limpiamos el input file por seguridad
        fileInput.value = '';
    } else {
        // MODO NUEVO
        title.innerHTML = '<i class="bi bi-plus-circle"></i> Nueva Plataforma';
        btn.textContent = 'Crear Plataforma';
        
        // Aseguramos que el hidden ID esté vacío
        document.getElementById('form_plataforma_id').value = '';

        // --- MANEJO DE LA IMAGEN EN MODO NUEVO ---
        previewContainer.style.display = 'none';
        logoPreview.src = '';
        
        // El input file empieza vacío
        fileInput.value = '';
    }

    modal.style.display = 'block';
}


// Función básica para cerrar
function cerrarModal() {
    const modal = document.getElementById('modalPlataforma');
    modal.style.display = 'none';
    // Opcional: limpiar el formulario al cerrar
    document.getElementById('formPlataforma').reset();
}

// 1. Cerrar al presionar la tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarModal();
    }
});

// 2. Cerrar al hacer clic fuera del contenido blanco (en el fondo oscuro)
window.onclick = function(event) {
    const modal = document.getElementById('modalPlataforma');
    if (event.target == modal) {
        cerrarModal();
    }
}

function confirmarEliminacion(nombre, urlEliminar) {
    if (confirm(`¿Estás seguro de que deseas eliminar la plataforma "${nombre}"?`)) {
        // Creamos un formulario temporal para enviar la petición POST de forma segura
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = urlEliminar; // <-- Aquí ya viene la URL correcta de Flask!
        document.body.appendChild(form);
        form.submit();
    }
}