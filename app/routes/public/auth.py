# app/routes/auth.py
# ===================================================================================================
import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services import UsuarioService
# ===================================================================================================
auth_bp = Blueprint('auth', __name__)
# ===================================================================================================
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    #  Login automatico
    if 'user_id' in session:
        return redirect(url_for('admin.index' if session['user_rol'] == 'admin' else 'user.dashboard'))
        
    # Validaciones y redireccion
    if request.method == 'POST':
        telefono = request.form.get('telefono', '').strip() # .strip() quita espacios accidentales
        password = request.form.get('password') # Este solo llega si se abrió el modal

        # 1. Validaciones entrada        
        if not telefono or not telefono.isdigit() or len(telefono) != 10:
            return render_template('public/login.html', error="Número inválido (10 dígitos)")
        

        # 2. Consultar en la DB
        user = UsuarioService.buscar_usuario(busqueda=telefono, exacto=True)

        if user:
            # Lógica para Admin
            if user.rol == 'admin':
                if password == os.getenv('ADMIN_PASSWORD'):
                    crear_sesion(user)
                    return redirect(url_for('admin.index'))
                return render_template('public/login.html', error="Contraseña admin incorrecta")
            
            # Lógica para Usuario (no_admin)
            crear_sesion(user)
            return redirect(url_for('user.dashboard')) # <--- Asegúrate que se llame 'dashboard' en user_routes
            
        return render_template('public/login.html', error="Este número no está registrado")
    return render_template('public/login.html')
# ===================================================================================================
@auth_bp.route('/logout')
def logout():
    """Cierra la sesión y redirige al login"""
    session.clear() # Borra todo el rastro del usuario en la sesión
    return redirect(url_for('auth.login'))
# ===================================================================================================
def crear_sesion(user):
    """Guarda los datos necesarios en la sesión de Flask"""
    session.clear() # Limpiamos sesiones previas por seguridad
    session.permanent = True # Esto respeta el tiempo de vida definido en el config (ej. 30 min)
    session['user_id'] = user.id
    session['user_rol'] = user.rol
    session['user_nombre'] = user.nombres
# ===================================================================================================    