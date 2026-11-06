/* ==================================================================================================== */
/* JAVASCRIPT: CONTROL DEL MODAL DE CARGOS EXTRAORDINARIOS */
/* ==================================================================================================== */

// 1. Abrir el modal nativo
function abrirModalCargoExtra() {
    document.getElementById('pbc-modal-cargo-extra').style.display = 'block';
    document.getElementById('formCargoExtra').reset();
    document.getElementById('divUsuariosCargo').style.display = 'none';
    cambiarPestana('usuario');
}

// 2. Cerrar el modal nativo
function cerrarModalCargoExtra() {
    document.getElementById('pbc-modal-cargo-extra').style.display = 'none';
}
function filtrarUsuariosCargo() {
    const plataformaSelect = document.getElementById('selectPlataformaCargo');
    const opcion = plataformaSelect.options[plataformaSelect.selectedIndex];
    const divUsuarios = document.getElementById('divUsuariosCargo');
    const usuarioSelect = document.getElementById('selectUsuarioCargo');
    const btnSubmit = document.getElementById('btnSubmitCargo');
    
    usuarioSelect.innerHTML = '';
    
    if (!opcion.value) {
        divUsuarios.style.display = 'none';
        usuarioSelect.disabled = true;  // ← Agregar
        return;
    }
    
    const usuarios = JSON.parse(opcion.getAttribute('data-usuarios') || '[]');
    
    divUsuarios.style.display = 'block';
    
    // Plataforma sin usuarios
    if (usuarios.length === 0) {
        btnSubmit.disabled = true;
        usuarioSelect.innerHTML = '<option value="">Sin usuarios en esta plataforma</option>';
        usuarioSelect.disabled = true;
        return;
    }
    
    btnSubmit.disabled = false;
    usuarioSelect.disabled = false;
    usuarioSelect.innerHTML = '<option value="">Seleccionar usuario...</option>';
    usuarios.forEach(u => {
        const opt = document.createElement('option');
        opt.value = u.id;
        opt.textContent = u.nombre;
        usuarioSelect.appendChild(opt);
    });
}

// 🔄 Aseguramos que al cambiar de pestaña el botón se resetee correctamente
function cambiarPestana(alcance) {
    document.getElementById('inputAlcance').value = alcance;
    const tabPlat = document.getElementById('tabPlataforma');
    const tabUser = document.getElementById('tabUsuario');
    const panelPlat = document.getElementById('panelPlataforma');
    const panelUser = document.getElementById('panelUsuario');
    const btnSubmit = document.getElementById('btnSubmitCargo');
    const selectPlatPanel = document.getElementById('selectPlataforma');

    if (alcance === 'plataforma') {
        tabPlat.classList.add('active');
        tabUser.classList.remove('active');
        panelPlat.style.setProperty('display', 'block', 'important');
        panelUser.style.setProperty('display', 'none', 'important');
        
        // Activar el select de plataforma del panel masivo (para que se envíe)
        selectPlatPanel.disabled = false;
        
        // Resetear el panel de usuario
        document.getElementById('divUsuariosCargo').style.display = 'none';
        document.getElementById('selectPlataformaCargo').disabled = true;
        document.getElementById('selectUsuarioCargo').disabled = true;
        
        btnSubmit.disabled = false;
    } else {
        tabUser.classList.add('active');
        tabPlat.classList.remove('active');
        panelUser.style.setProperty('display', 'block', 'important');
        panelPlat.style.setProperty('display', 'none', 'important');
        
        // Deshabilitar el select del panel masivo (para que NO se envíe)
        selectPlatPanel.disabled = true;
        
        // Resetear el panel de usuario
        document.getElementById('divUsuariosCargo').style.display = 'none';
        document.getElementById('selectUsuarioCargo').innerHTML = '';
        document.getElementById('selectUsuarioCargo').disabled = true;
        document.getElementById('selectPlataformaCargo').value = '';  // ← Agregar
        document.getElementById('selectPlataformaCargo').disabled = false;

        
        btnSubmit.disabled = false;
    }
}

// 4. Cerrar el modal automáticamente si el administrador da clic afuera del recuadro blanco
window.onclick = function(event) {
    const modal = document.getElementById('pbc-modal-cargo-extra');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Gestiona las listas desplegables de los users con varios pagos
function toggleGrupo(fila) {
    const icono = fila.querySelector('.bi-chevron-down, .bi-chevron-up');
    let siguiente = fila.nextElementSibling;
    
    while (siguiente && siguiente.classList.contains('pbc-sub-row')) {
        siguiente.style.display = siguiente.style.display === 'none' ? 'table-row' : 'none';
        siguiente = siguiente.nextElementSibling;
    }
    
    if (icono) {
        icono.classList.toggle('bi-chevron-down');
        icono.classList.toggle('bi-chevron-up');
    }
}

function confirmarEliminarCobro(motivo, urlEliminar) {
    if (confirm(`¿Estás seguro de que deseas eliminar el cobro "${motivo}"?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = urlEliminar;
        document.body.appendChild(form);
        form.submit();
    }
}

function abrirModalEditar(cobroId, plataforma, motivo, monto) {
    document.getElementById('edit_cobro_id').value = cobroId;
    document.getElementById('edit_plataforma').value = plataforma;
    document.getElementById('edit_motivo').value = motivo || '';
    document.getElementById('edit_monto').value = monto;
    
    document.getElementById('formEditarCobro').action = `/admin/cobros/editar/${cobroId}`;
    
    const modal = new bootstrap.Modal(document.getElementById('modalEditarCobro'));
    modal.show();
}

function cerrarModalEditar() {
    const modal = document.getElementById('modalEditarCobro');
    modal.style.display = 'none';
    document.getElementById('formEditarCobro').reset();
}

// Cerrar con ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarModalEditar();
        cerrarModalRevision();
    }
});

// Cerrar al hacer clic fuera del modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalEditarCobro');
    if (event.target === modal) {
        cerrarModalEditar();
    }
});

// Cerrar modal cargo extra con ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarModalCargoExtra();
    }
});

// Cerrar modal cargo extra al hacer clic fuera
window.addEventListener('click', function(event) {
    const modal = document.getElementById('pbc-modal-cargo-extra');
    if (event.target === modal) {
        cerrarModalCargoExtra();
    }
});