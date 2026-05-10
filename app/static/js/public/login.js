const celularInput = document.getElementById('telefono');
const adminModal = document.getElementById('adminModal');
const loginForm = document.getElementById('loginForm');
const adminPassInput = document.getElementById('adminPass');

const ADMIN_NUMBER = "7774399424"; 

// 1. Escuchador para el primer paso (Continuar)
loginForm.addEventListener('submit', (e) => {
    const valorCelular = celularInput.value.trim();

    if (valorCelular === ADMIN_NUMBER) {
        e.preventDefault(); // Detenemos el envío para mostrar el modal
        adminModal.style.display = 'flex';
        adminPassInput.focus();
    }
    // Si no es admin, el e.preventDefault no se ejecuta y el form se va directo.
});

// 2. Función para el envío FINAL desde el modal
function submitFinal() {
    if (adminPassInput.value.trim() === "") {
        alert("Por favor, ingresa la clave maestra.");
        return;
    }
    // Esto envía el formulario saltándose el EventListener anterior
    loginForm.submit(); 
}

function closeModal() {
    adminModal.style.display = 'none';
    adminPassInput.value = "";
}

window.onclick = function(event) {
    if (event.target == adminModal) { closeModal(); }
}

// 3. Permitir que el "Enter" envíe el formulario desde el campo de password
adminPassInput.addEventListener('keydown', (e) => {
    if (e.key === "Enter") {
        e.preventDefault(); // Evitamos cualquier comportamiento extraño
        submitFinal();      // Llamamos a tu función que hace el loginForm.submit()
    }
});