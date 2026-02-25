function expandirImagen(elemento) {
    // Verificamos si la imagen tiene un SRC válido antes de intentar ampliar
    if (!elemento.src || elemento.src.includes('undefined') || elemento.src === window.location.href) {
        console.warn("No hay imagen cargada para expandir.");
        return;
    }

    if (!document.fullscreenElement) {
        // Entrar en pantalla completa
        if (elemento.requestFullscreen) {
            elemento.requestFullscreen();
        } else if (elemento.webkitRequestFullscreen) { /* Safari / Chrome antiguo */
            elemento.webkitRequestFullscreen();
        } else if (elemento.msRequestFullscreen) { /* IE11 */
            elemento.msRequestFullscreen();
        }
    } else {
        // Salir de pantalla completa si ya está dentro
        document.exitFullscreen();
    }
}