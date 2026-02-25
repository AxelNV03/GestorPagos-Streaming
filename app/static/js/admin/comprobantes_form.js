function openUpMgr(id, user, amount, userId) {
    document.getElementById('up-mgr-id').value = id;
    document.getElementById('up-mgr-user').innerText = user;
    document.getElementById('up-mgr-amount').innerText = amount;
    document.getElementById('upMgrModal').style.display = 'flex';
    document.getElementById('up-mgr-user-id').value = userId; // Inyectamos el ID del usuario
}

function closeUpMgr() {
    document.getElementById('upMgrModal').style.display = 'none';
}

// Escuchar clics fuera del modal para cerrar
window.onclick = function(event) {
    let modal = document.getElementById('upMgrModal');
    if (event.target == modal) closeUpMgr();
}


document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        const modal = document.getElementById('upMgrModal');
        // Solo cerramos si el modal tiene el display en 'flex' o 'block'
        if (modal.style.display === 'flex' || modal.style.display === 'block') {
            closeUpMgr();
        }
    }
});