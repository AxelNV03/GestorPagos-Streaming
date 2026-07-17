/* ==================================================================================================== */
/* JAVASCRIPT: CONTROL DEL MODAL DE CARGOS EXTRAORDINARIOS */
/* ==================================================================================================== */

// 1. Abrir el modal nativo
function abrirModalCargoExtra() {
    document.getElementById('pbc-modal-cargo-extra').style.display = 'block';
    cambiarPestana('usuario');
}

// 2. Cerrar el modal nativo
function cerrarModalCargoExtra() {
    document.getElementById('pbc-modal-cargo-extra').style.display = 'none';
}
function mostrarPlataformasLocales(selectElement) {
    const contenedor = document.getElementById('divPlataformasDelUsuario');
    const btnSubmit = document.getElementById('btnSubmitCargo');
    const opcionSeleccionada = selectElement.options[selectElement.selectedIndex];
    
    if (!opcionSeleccionada.value) {
        contenedor.style.display = 'none';
        contenedor.innerHTML = '';
        btnSubmit.disabled = false; // Estado por defecto
        return;
    }

    const plataformas = JSON.parse(opcionSeleccionada.getAttribute('data-plataformas') || '[]');
    contenedor.style.display = 'block';

    // 🔴 Caso A: El usuario NO tiene plataformas asociadas
    if (plataformas.length === 0) {
        btnSubmit.disabled = true; // 🔒 BLOQUEAMOS EL BOTÓN
        contenedor.innerHTML = `
            <div style="background:#fff5f5; border: 1px solid #fed7d7; padding: 12px; border-radius: 6px; color: #c53030; font-size: 0.85rem;">
                ⚠️ <strong>Atención:</strong> Este usuario no tiene ninguna plataforma asociada. No se puede generar un cargo.
            </div>
        `;
    } 
    // 🟢 Caso B: El usuario SÍ tiene plataformas asociadas
    else {
        btnSubmit.disabled = false; // 🔓 DESBLOQUEAMOS EL BOTÓN
        let options = '<option value="" selected disabled>-- Selecciona la plataforma para el cobro --</option>';
        plataformas.forEach(p => {
            options += `<option value="${p.id}">${p.nombre}</option>`;
        });

        contenedor.innerHTML = `
            <label>Selecciona la plataforma asociada</label>
            <select class="pbc-form-select" name="plataforma_id" required>
                ${options}
            </select>
        `;
    }
}

// 🔄 Aseguramos que al cambiar de pestaña el botón se resetee correctamente
function cambiarPestana(alcance) {
    document.getElementById('inputAlcance').value = alcance;
    const tabPlat = document.getElementById('tabPlataforma');
    const tabUser = document.getElementById('tabUsuario');
    const panelPlat = document.getElementById('panelPlataforma');
    const panelUser = document.getElementById('panelUsuario');
    const btnSubmit = document.getElementById('btnSubmitCargo');

    if (alcance === 'plataforma') {
        tabPlat.classList.add('active');
        tabUser.classList.remove('active');
        panelPlat.style.setProperty('display', 'block', 'important');
        panelUser.style.setProperty('display', 'none', 'important');
        
        btnSubmit.disabled = false; // Al pasar a masivo por plataforma siempre se desbloquea
    } else {
        tabUser.classList.add('active');
        tabPlat.classList.remove('active');
        panelUser.style.setProperty('display', 'block', 'important');
        panelPlat.style.setProperty('display', 'none', 'important');
        
        // Volvemos a evaluar según el select de usuarios actual
        const selectUser = document.getElementById('selectUsuario');
        mostrarPlataformasLocales(selectUser);
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
    }
});

// Cerrar al hacer clic fuera del modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalEditarCobro');
    if (event.target === modal) {
        cerrarModalEditar();
    }
});