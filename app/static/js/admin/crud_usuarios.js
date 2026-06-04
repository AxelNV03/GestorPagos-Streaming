// ===================================================================================================
// Lógica para los botones dinámicos (Agregar/Quitar Filas)
// ===================================================================================================
document.addEventListener("DOMContentLoaded", function() {
    const contenedor = document.getElementById("contenedor-plataformas");
    const btnAgregar = document.getElementById("btn-agregar-plataforma");
    const molde = document.getElementById("molde-plataforma");

    // 1. Escuchar el clic para Agregar una nueva fila de plataforma
    btnAgregar.addEventListener("click", function() {
        // Clonamos el contenido interno del <template> (true significa clonar con hijos)
        const clon = molde.content.cloneNode(true);
        // Lo metemos al contenedor visible
        contenedor.appendChild(clon);
    });

    // 2. Escuchar el clic para Eliminar una fila (Usamos delegación de eventos)
    contenedor.addEventListener("click", function(event) {
        // Buscamos si el clic fue en el botón de basura o en el icono de adentro
        const botonQuitar = event.target.closest(".btn-quitar-plataforma");
        
        if (botonQuitar) {
            // Buscamos la fila contenedora más cercana y la removemos del HTML
            const fila = botonQuitar.closest(".fila-plataforma");
            if (fila) {
                fila.remove();
            }
        }
    });
});

// ===================================================================================================
// Lógica Crear y Editar Usuarios
// ===================================================================================================

// Variable global o listener para controlar los botones de agregar/quitar
function abrirModalUsuario(data = {}) {
    const modal = document.getElementById('modalUsuario');
    const form = document.getElementById('formUsuario');
    const title = document.getElementById('modalTitle');
    const btn = document.getElementById('btnGuardar');
    const contenedorPlat = document.getElementById("contenedor-plataformas");

    // Limpiamos el formulario por si acaso
    form.reset();
    contenedorPlat.innerHTML = "";

    if (data.id) {
        // MODO EDICIÓN
        title.innerHTML = '<i class="bi bi-pencil-square"></i> Editar Usuario';
        btn.textContent = 'Actualizar Usuario';

        // Rellenar Campos
        document.getElementById('form_usuario_id').value = data.id;
        document.getElementById('form_nombres').value = data.nombres;
        document.getElementById('form_apeP').value = data.apeP;
        document.getElementById('form_apeM').value = data.apeM;
        document.getElementById('form_telefono').value = data.telefono;
        document.getElementById('form_correo').value = data.correo;


        // Plataformas
        if (data.plataformas && data.plataformas.length > 0) {
            const molde = document.getElementById('molde-plataforma');

            data.plataformas.forEach(platId => {
                // 1. Clonamos el contenido del molde HTML
                const clon = molde.content.cloneNode(true);
                
                // 2. Buscamos el elemento <select> dentro del clon
                const select = clon.querySelector('select[name="plataformas[]"]');
                
                // 3. Le asignamos el ID de la plataforma para que aparezca seleccionada
                select.value = platId;
                
                // 4. Lo inyectamos en el contenedor visual del modal
                contenedorPlat.appendChild(clon);
            });
        }

    } else {
        // Modo Nuevo
        title.innerHTML = '<i class="bi bi-plus-circle"></i> Nuevo Usuario';
        btn.textContent = 'Guardar Usuario';
        
        // Aseguramos que el hidden ID esté vacío
        document.getElementById('form_usuario_id').value = '';
    }
    
    modal.style.display = 'block';
}


// Función básica para cerrar
function cerrarModal() {
    const modal = document.getElementById('modalUsuario');
    modal.style.display = 'none';
    // Opcional: limpiar el formulario al cerrar
    document.getElementById('formUsuario').reset();
    document.getElementById("contenedor-plataformas").innerHTML = "";
}

// 1. Cerrar al presionar la tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarModal();
    }
});

// 2. Cerrar al hacer clic fuera del contenido blanco (en el fondo oscuro)
window.onclick = function(event) {
    const modal = document.getElementById('modalUsuario');
    if (event.target == modal) {
        cerrarModal();
    }
}

function confirmarEliminacion(nombre, urlEliminar) {
    if (confirm(`¿Estás seguro de que deseas eliminar el usuario "${nombre}"?`)) {
        // Creamos un formulario temporal para enviar la petición POST de forma segura
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = urlEliminar; // <-- Aquí ya viene la URL correcta de Flask!
        document.body.appendChild(form);
        form.submit();
    }
}