function abrirModalAnuncio() {
    document.getElementById('pbc-modal-anuncio').style.display = 'block';
    cambiarPestanaAnuncio('plataforma');
}

function cerrarModalAnuncio() {
    document.getElementById('pbc-modal-anuncio').style.display = 'none';
}

function cambiarPestanaAnuncio(alcance) {
    document.getElementById('inputAlcanceAnuncio').value = alcance;
    const tabPlat = document.getElementById('tabPlataformaAnuncio');
    const tabUser = document.getElementById('tabUsuarioAnuncio');
    const panelPlat = document.getElementById('panelPlataformaAnuncio');
    const panelUser = document.getElementById('panelUsuarioAnuncio');

    if (alcance === 'plataforma') {
        tabPlat.classList.add('active');
        tabUser.classList.remove('active');
        panelPlat.style.setProperty('display', 'block', 'important');
        panelUser.style.setProperty('display', 'none', 'important');
    } else {
        tabUser.classList.add('active');
        tabPlat.classList.remove('active');
        panelUser.style.setProperty('display', 'block', 'important');
        panelPlat.style.setProperty('display', 'none', 'important');
    }
}
// Cerrar con ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarModalAnuncio();
    }
});

// Cerrar al hacer clic fuera
window.addEventListener('click', function(event) {
    const modal = document.getElementById('pbc-modal-anuncio');
    if (event.target === modal) {
        cerrarModalAnuncio();
    }
});