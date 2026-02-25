function abrirVisorNota(boton) {
    // Extraemos el texto del atributo data-nota del botón que fue clickeado
    const texto = boton.getAttribute('data-nota');
    const p = document.getElementById('textoNotaCompleta');
    
    if (!texto || texto === 'None' || texto.trim() === "") {
        p.innerHTML = `<span style="color: #94a3b8; font-style: italic;">Sin observaciones del cliente.</span>`;
    } else {
        p.innerText = texto;
    }

    // Mostramos el modal
    document.getElementById('modalNotaDetalle').style.display = 'flex';
}

function cerrarModalNota() {
    document.getElementById('modalNotaDetalle').style.display = 'none';
}

// --- Soporte para ESC y Clic fuera ---
document.addEventListener('keydown', (e) => {
    if (e.key === "Escape") cerrarModalNota();
});

document.addEventListener('click', (e) => {
    const modal = document.getElementById('modalNotaDetalle');
    if (e.target === modal) cerrarModalNota();
});