
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
    
    // Limpiar comentario
    document.getElementById('cpc_rev_comentario').value = '';
    
    const seccionAsignaciones = document.getElementById('cpc_rev_asignaciones');
    const seccionResultado = document.getElementById('cpc_rev_resultado');
    const seccionComentario = document.getElementById('cpc_rev_seccion_comentario');
    const resumen = document.getElementById('cpc_rev_resumen');
    const footer = document.querySelector('.cpc-revision-footer');
    
    if (comp.estado === 'revision') {
        // Modo revisión: mostrar asignaciones
        seccionAsignaciones.style.display = 'block';
        seccionResultado.style.display = 'none';
        seccionComentario.style.display = 'block';
        resumen.style.display = 'block';
        footer.style.display = 'flex';
        
        if (pendientes) {
            renderMensualidadesRevision(pendientes.mensualidades);
            renderExtrasRevision(pendientes.extras);
        }
    } else {
        // Modo solo lectura
        seccionAsignaciones.style.display = 'none';
        seccionResultado.style.display = 'block';
        seccionComentario.style.display = 'none';
        resumen.style.display = 'none';
        footer.style.display = 'none';
        
        // Fecha de carga
        if (comp.fecha_carga) {
            const fecha = new Date(comp.fecha_carga);
            const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            document.getElementById('cpc_rev_fecha').textContent = fecha.toLocaleDateString('es-MX', opciones);
        }
        
        // Pagos cubiertos (solo aprobado)
        const pagosCubiertos = document.getElementById('cpc_rev_pagos_cubiertos');
        if (comp.estado === 'aprobado' && pendientes) {
            pagosCubiertos.style.display = 'block';
            pagosCubiertos.style.display = 'block';
            renderCobrosAsociados(comp.cobros_asociados);
        } else {
            pagosCubiertos.style.display = 'none';
        }
        
        // Motivo / Comentario
        const label = document.getElementById('cpc_rev_resultado_label');
        const texto = document.getElementById('cpc_rev_resultado_texto');
        
        if (comp.estado === 'rechazado') {
            label.textContent = 'Motivo de rechazo';
            texto.textContent = comp.motivo_rechazo || 'Sin motivo';
        } else {
            label.textContent = 'Comentario';
            texto.textContent = comp.comentario || 'Sin comentario';
        }
    }
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
    
    div.innerHTML = mensualidades.map(m => {
        const opciones = Array.from({length: 13}, (_, i) => 
            `<option value="${i}">${i} ${i === 1 ? 'mes' : 'meses'} - $${(m.costo_mensual * i).toFixed(2)}</option>`
        ).join('');
        
        return `
            <div class="cpc-form-group">
                <label>${m.plataforma} <small style="font-weight:400;color:#94a3b8;">| Último: ${m.ultimo_pago || 'N/A'}</small></label>
                <select name="meses_${m.plataforma_usuario_id}" class="cpc-form-select cpc-mes-select" data-costo="${m.costo_mensual}" onchange="actualizarResumen()">
                    ${opciones}
                </select>
            </div>
        `;
    }).join('');
    
    actualizarResumen();
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
                <input type="checkbox" name="extra_${e.cobro_id}" value="${e.monto}" data-monto="${e.monto}" onchange="actualizarResumen()">
                <span class="cpc-extra-slider"></span>
            </label>
        </div>
    `).join('');
    
    actualizarResumen();
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

// ===================================================================
// ACCIONES DEL MODAL
// ===================================================================

function accionComprobante(accion) {
    const comprobanteId = document.getElementById('modalRevision').dataset.comprobanteId;
    const comentario = document.getElementById('cpc_rev_comentario').value;
    
    // Validaciones
    if (accion === 'rechazar') {
        if (!comentario.trim()) {
            alert('Debe ingresar un motivo de rechazo');
            return;
        }
        if (!confirm('¿Está seguro de rechazar este comprobante?')) return;
    }
    
    if (accion === 'aprobar') {
        // Verificar que al menos haya algo seleccionado
        let haySeleccion = false;
        
        document.querySelectorAll('.cpc-mes-select').forEach(select => {
            if (parseInt(select.value) > 0) haySeleccion = true;
        });
        document.querySelectorAll('.cpc-extra-switch input:checked').forEach(() => {
            haySeleccion = true;
        });
        
        if (!haySeleccion) {
            alert('Debe seleccionar al menos un mes o un extra para aprobar');
            return;
        }
        
        if (!confirm('¿Está seguro de aprobar este comprobante?')) return;
    }
    
    // Crear formulario
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/admin/comprobantes/${accion === 'rechazar' ? 'rechazar' : 'aprobar'}/${comprobanteId}`;
    
    // Comentario
    const inputComentario = document.createElement('input');
    inputComentario.type = 'hidden';
    inputComentario.name = 'comentario';
    inputComentario.value = comentario;
    form.appendChild(inputComentario);
    
    // Mensualidades y extras (solo para aprobar)
    if (accion === 'aprobar') {
        document.querySelectorAll('.cpc-mes-select').forEach(select => {
            if (parseInt(select.value) > 0) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = select.name;
                input.value = select.value;
                form.appendChild(input);
            }
        });
        
        document.querySelectorAll('.cpc-extra-switch input:checked').forEach(checkbox => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = checkbox.name;
            input.value = '1';
            form.appendChild(input);
        });
    }
    
    document.body.appendChild(form);
    form.submit();
}

function actualizarResumen() {
    let total = 0;
    
    // Sumar mensualidades seleccionadas
    document.querySelectorAll('.cpc-mes-select').forEach(select => {
        const meses = parseInt(select.value) || 0;
        const costo = parseFloat(select.dataset.costo) || 0;
        total += costo * meses;
    });
    
    // Sumar extras con checkbox ON
    document.querySelectorAll('.cpc-extra-switch input:checked').forEach(checkbox => {
        const monto = parseFloat(checkbox.dataset.monto) || 0;
        total += monto;
    });
    
    document.getElementById('cpc_resumen_total').textContent = `$${total.toFixed(2)}`;
}


function renderCobrosAsociados(cobros) {
    const MESES_ES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
    const MESES_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    
    const traducirMes = (fecha) => {
        if (!fecha) return '';
        const partes = fecha.split(' ');
        if (partes.length === 2) {
            const idx = MESES_EN.indexOf(partes[0]);
            return idx !== -1 ? `${MESES_ES[idx]} ${partes[1]}` : fecha;
        }
        return fecha;
    };
    
    const mensualidades = cobros.filter(c => c.motivo.startsWith('Mensualidad'));
    const extras = cobros.filter(c => !c.motivo.startsWith('Mensualidad'));
    
    document.getElementById('cpc_rev_mensualidades_cubiertas').innerHTML = mensualidades.length 
        ? '<div class="cpc-pagos-lista">' + mensualidades.map(c => `
            <div class="cpc-pago-item">
                <span class="cpc-pago-item-plataforma">${c.plataforma}</span>
                <span class="cpc-pago-item-detalle">${traducirMes(c.mes_anio)}</span>
            </div>
        `).join('') + '</div>'
        : '<p class="pbc-txt-muted">Sin mensualidades</p>';
    
    document.getElementById('cpc_rev_extras_cubiertos').innerHTML = extras.length 
        ? '<div class="cpc-pagos-lista">' + extras.map(c => `
            <div class="cpc-pago-item">
                <span class="cpc-pago-item-plataforma">${c.plataforma}</span>
                <span class="cpc-pago-item-detalle">${c.motivo}</span>
            </div>
        `).join('') + '</div>'
        : '<p class="pbc-txt-muted">Sin extras</p>';
}