
// ===================================================================
// MODAL NUEVO COMPROBANTE
// ===================================================================

function abrirModalNuevoComprobante() {
    document.getElementById('modalNuevoComprobante').style.display = 'block';
    document.getElementById('formNuevoComprobante').reset();
    document.getElementById('cpc_file_name').textContent = 'Seleccionar imagen...';
}

function cerrarModalNuevoComprobante() {
    document.getElementById('modalNuevoComprobante').style.display = 'none';
    document.getElementById('formNuevoComprobante').reset();
}

// Mostrar nombre del archivo seleccionado
document.getElementById('cpc_file_input').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'Seleccionar imagen...';
    document.getElementById('cpc_file_name').textContent = fileName;
});

// Cerrar con ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        cerrarModalNuevoComprobante();
    }
});

// Cerrar al hacer clic fuera
window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalNuevoComprobante');
    if (event.target === modal) {
        cerrarModalNuevoComprobante();
    }
});

// ===================================================================
// MODAL REVISIÓN COMPROBANTE
// ===================================================================

function revisarComprobante(comprobanteId) {
    const comp = infoComprobantes[comprobanteId];
    const pendientes = datosRevision[comprobanteId];
    
    if (!comp) return;
    
    // Imagen
    document.getElementById('cpc_rev_imagen').src = comp.imagen_url;
    
    // Usuario
    document.getElementById('cpc_rev_usuario').textContent = comp.usuario;
    
    // Nota
    document.getElementById('cpc_rev_nota').textContent = comp.nota || 'Sin nota';
    
    // Estado
    const estadoEl = document.getElementById('cpc_rev_estado');
    estadoEl.textContent = comp.estado === 'revision' ? 'En Revisión' : 
                           comp.estado === 'aprobado' ? 'Aprobado' : 'Rechazado';
    
    // Mensualidades y extras
    if (pendientes) {
        renderMensualidadesRevision(pendientes.mensualidades);
        renderExtrasRevision(pendientes.extras);
    }
    
    // Botones solo en revisión
    const footer = document.querySelector('.cpc-revision-footer');
    footer.style.display = comp.estado === 'revision' ? 'flex' : 'none';
    
    // Limpiar comentario
    document.getElementById('cpc_rev_comentario').value = '';
    
    // Guardar ID
    document.getElementById('modalRevision').dataset.comprobanteId = comprobanteId;
    document.getElementById('modalRevision').style.display = 'block';
}

function cerrarModalRevision() {
    document.getElementById('modalRevision').style.display = 'none';
}

function renderMensualidadesRevision(mensualidades) {
    const div = document.getElementById('cpc_rev_mensualidades');
    
    if (!mensualidades || !mensualidades.length) {
        div.innerHTML = '<div class="cpc-empty-asignaciones">Sin mensualidades pendientes</div>';
        return;
    }
    
    div.innerHTML = mensualidades.map(m => `
        <div class="cpc-form-group">
            <label>${m.plataforma} <small style="font-weight:400;color:#94a3b8;">| Último: ${m.ultimo_pago || 'N/A'}</small></label>
            <select name="meses_${m.plataforma_usuario_id}" class="cpc-form-select">
                <option value="0">0 meses</option>
                <option value="1">1 mes</option>
                <option value="2">2 meses</option>
                <option value="3">3 meses</option>
                <option value="4">4 meses</option>
                <option value="5">5 meses</option>
                <option value="6">6 meses</option>
                <option value="7">7 meses</option>
                <option value="8">8 meses</option>
                <option value="9">9 meses</option>
                <option value="10">10 meses</option>
                <option value="11">11 meses</option>
                <option value="12">12 meses</option>
            </select>
        </div>
    `).join('');
}

function renderExtrasRevision(extras) {
    const div = document.getElementById('cpc_rev_extras');
    
    if (!extras || !extras.length) {
        div.innerHTML = '<div class="cpc-empty-asignaciones">Sin extras pendientes</div>';
        return;
    }
    
    div.innerHTML = extras.map(e => `
        <div class="cpc-extra-card">
            <div class="cpc-extra-card-left">
                <span class="cpc-extra-plataforma">${e.plataforma}</span>
                <span class="cpc-extra-concepto">${e.concepto}</span>
            </div>
            <span class="cpc-extra-monto">$${e.monto.toFixed(2)}</span>
            <label class="cpc-extra-switch">
                <input type="checkbox" name="extra_${e.cobro_id}" value="1">
                <span class="cpc-extra-slider"></span>
            </label>
        </div>
    `).join('');
}

// Cerrar con ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        cerrarModalRevision();
    }
});

// Cerrar al hacer clic fuera
window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalRevision');
    if (event.target === modal) {
        cerrarModalRevision();
    }
});