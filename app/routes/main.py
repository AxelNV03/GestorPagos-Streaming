# app/routes/main.py
# ===================================================================================================
import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services import UserService
# ===================================================================================================
main_bp = Blueprint('main', __name__)
# ===================================================================================================
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    # Credenciales del .env
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    
    # Validaciones y redireccion
    if request.method == 'POST':
        telefono = request.form.get('telefono', '').strip() # .strip() quita espacios accidentales
        password = request.form.get('password') # Este solo llega si se abrió el modal

        # 1. Validaciones entrada
        if not telefono:
            return render_template('login.html', error="Introduce un número")
        if not telefono.isdigit() or len(telefono) != 10:
            return render_template('login.html', error="Número inválido (debe tener 10 dígitos)")
        
        # 2. Consultar en la DB
        user = UserService.buscar_usuario(tel=telefono)

        if user:
            # 4. Verificación de Roles
            if user.rol == 'admin':
                # Si es admin, validamos la contraseña
                if password == ADMIN_PASSWORD:
                    crear_sesion(user)
                    return redirect(url_for('admin.dashboard'))
                else:
                    return render_template('login.html', error="Contraseña de administrador incorrecta")
            
            
            # 5. Si es un usuario normal (cliente), entra directo por teléfono
            crear_sesion(user)
            return redirect(url_for('user.dashboard'))
        else:
            return render_template('login.html', error="Este número no está registrado")
    return render_template('login.html')
# ===================================================================================================
@main_bp.route('/logout')
def logout():
    """Cierra la sesión y redirige al login"""
    session.clear() # Borra todo el rastro del usuario en la sesión
    return redirect(url_for('main.login'))
# ===================================================================================================
def crear_sesion(user):
    """Guarda los datos necesarios en la sesión de Flask"""
    session.clear() # Limpiamos sesiones previas por seguridad
    session['user_id'] = user.id
    session['user_rol'] = user.rol
    session['user_nombre'] = user.nombres
    