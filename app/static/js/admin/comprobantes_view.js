let currentVisorId = null;

function mostrarComprobante(ruta, id, estado, usuario, monto, boton) {    
    const notaRecibida = boton.getAttribute('data-nota');
    currentVisorId = id;
    // Rellenar datos en el modal
    document.getElementById('visor-user').innerText = usuario;
    document.getElementById('visor-amount').innerText = monto;
    document.getElementById('imgComprobanteVisor').src = `/admin/comprobante/archivo/${ruta}`;

    // 2. Elementos del modal
    const disparadorModal = document.getElementById('nota-icono-modal');
    const iconoAlerta = document.getElementById('icono-alerta');
    const iconoMensaje = document.getElementById('icono-mensaje');

    // 3. Tu Validación: Si nota no es nula, ni vacía, ni dice "ninguna"
    const tieneNotaReal = notaRecibida && 
                          notaRecibida.trim() !== "" && 
                          notaRecibida.toLowerCase() !== "ninguna" && 
                          notaRecibida !== "None";

    // 4. Aplicar lógica de iconos
    disparadorModal.setAttribute('data-nota', notaRecibida); // Pasamos la nota al data-nota

    if (tieneNotaReal) {
        iconoAlerta.style.display = 'block';  // Muestra el círculo (!)
        iconoMensaje.style.display = 'none';
    } else {
        iconoAlerta.style.display = 'none';
        iconoMensaje.style.display = 'block'; // Muestra el sobre tenue
    }

    
    // Controlar visibilidad de acciones
    const seccionAcciones = document.getElementById('visor-acciones');
    if (estado !== 'pagado' && estado !== 'rechazado') {
        seccionAcciones.style.display = 'block';
    } else {
        seccionAcciones.style.display = 'none';
    }

    // Mostrar el modal (usando el estilo de tu overlay)
    document.getElementById('visorComprobanteModal').style.display = 'flex';
}

function procesarPago(accion) {
    const meses = document.getElementById('visor-meses').value;
    
    if (accion === 'rechazar') {
        if (!confirm("¿Seguro que deseas rechazar este pago?")) return;
    }
    
    // Aquí el console log para probar en tu Thinkpad
    console.log(`Acción: ${accion}, ID Cobro: ${currentVisorId}, Meses: ${meses}`);
    
    // Ejemplo de envío (ajusta a tu ruta)
    /*
    fetch('/admin/validar_pago', {
        method: 'POST',
        body: JSON.stringify({ id: currentVisorId, accion: accion, meses: meses })
    }).then(res => location.reload());
    */
}

function cerrarVisor() {
    document.getElementById('visorComprobanteModal').style.display = 'none';
}

// --- EVENTOS DE CIERRE ---

// 1. Cerrar con la tecla ESC
document.addEventListener('keydown', function(e) {
    if (e.key === "Escape") {
        const modal = document.getElementById('visorComprobanteModal');
        // Solo cerramos si el modal está visible (display: flex)
        if (window.getComputedStyle(modal).display === 'flex') {
            cerrarVisor();
        }
    }
});

// 2. Cerrar al hacer clic fuera (en el overlay oscuro)
document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('visorComprobanteModal');
    
    modalOverlay.addEventListener('click', function(e) {
        // 'this' es el overlay. Si el clic fue exactamente ahí y no en sus hijos:
        if (e.target === this) {
            cerrarVisor();
        }
    });
});