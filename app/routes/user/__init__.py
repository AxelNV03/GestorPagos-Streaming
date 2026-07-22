from flask import Blueprint, session, redirect, url_for, flash

# 1. Definimos el Blueprint que agrupa todo el módulo de usuario
user_bp = Blueprint('user', __name__)

# 2. Filtro de seguridad global exclusivo para el Blueprint de usuarios
@user_bp.before_request
def restringir_acceso_user():
    """Bloquea el acceso a cualquier ruta de este Blueprint si no es un usuario común."""
    # Verificar si el usuario ha iniciado sesión
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para acceder.", "warning")
        return redirect(url_for('auth.login'))
        
    # Verificar el rol asignado en la sesión
    rol_actual = session.get('user_rol')
    
    # Si un administrador intenta ingresar al panel de usuarios, lo redirigimos a su panel
    if rol_actual == 'admin':
        return redirect(url_for('admin.cobros'))
        
    # Si no es un usuario autorizado ('no_admin'), lo regresamos al login
    if rol_actual != 'no_admin':
        flash("Acceso denegado: Rol no válido.", "danger")
        return redirect(url_for('auth.login'))

# 3. Importamos las rutas específicas (evita importación circular)
from . import dashboard