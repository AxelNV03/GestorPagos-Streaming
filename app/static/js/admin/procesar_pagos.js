function procesarPago(accion) {
    // 1. Verificamos que tengamos el ID (importante)
    if (!currentVisorId) {
        alert("Error: No se encontró el ID del pago.");
        return;
    }

    // 2. Confirmación visual
    const confirmacion = accion === 'rechazar' 
        ? confirm("¿Seguro que deseas rechazar este pago?") 
        : true; // Para aprobar no pedimos confirmación (opcional)

    if (!confirmacion) return;

    // 3. Capturamos el formulario
    const formulario = document.getElementById('form-gestion-pago');

    // 4. Si tienes el input de meses, podemos pasarlo como parámetro en la URL 
    // o simplemente dejar que Python lo ignore si no lo usas aún.
    // Construimos la URL de acción del formulario
    formulario.action = `/admin/pago/${accion}/${currentVisorId}`;

    // 5. ¡Lanzamos el formulario! 
    // Esto hará que el navegador navegue de verdad, permitiendo que el FLASH funcione.
    formulario.submit();
}