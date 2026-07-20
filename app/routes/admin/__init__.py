from flask import Blueprint, session, redirect, url_for, flash

# 1. Definimos el Blueprint que agrupa todo
admin_bp = Blueprint('admin', __name__)

# 2. Filtro de seguridad global exclusivo para este Blueprint
@admin_bp.before_request
def restringir_acceso_admin():
    """Bloquea el acceso a cualquier ruta de este Blueprint si no es admin."""
    # Verificar si el usuario ha iniciado sesión
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para acceder.", "warning")
        return redirect(url_for('auth.login'))
        
    # Verificar si el rol guardado en sesión es estrictamente 'admin'
    if session.get('user_rol') != 'admin':
        flash("Acceso denegado: Se requieren permisos de administrador.", "danger")
        # Si es un usuario común ('no_admin'), podrías mandarlo a su panel index o al login
        return redirect(url_for('auth.login'))

# 2. Importamos las rutas específicas (esto evita problemas de importación circular)
from . import dashboard
from . import plataformas
from . import usuarios
from . import cobros
from . import comprobantes