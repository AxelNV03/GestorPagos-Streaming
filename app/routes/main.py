# app/routes/main.py
# ===================================================================================================
import os  # <--- AGREGA ESTA LÍNEA AQUÍ
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from app.services import UserService
# ===================================================================================================
main_bp = Blueprint('main', __name__)
# ===================================================================================================
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    # Credenciales
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    
    # Validaciones y redireccion
    if request.method == 'POST':
        telefono = request.form.get('telefono', '').strip() # .strip() quita espacios accidentales
        password = request.form.get('password') # Este solo llega si se abrió el modal

        # 1. Validaciones
        if not telefono:
            return render_template('login.html', error="Introduce un número")
        if not telefono.isdigit():
            return render_template('login.html', error="Solo se permiten números")
        if len(telefono) != 10:
            return render_template('login.html', error="El número debe ser de 10 dígitos")
        
        # 2. Todo valido ejecuta consulta
        users_data = UserService()
        user = users_data.buscar_usuario(tel=telefono)

        if user:
            # Datos de la sesión
            session['user_id'] = user['id']
            session['user_rol'] = user['rol'] # 'admin' o 'no_admin'

            if user['rol'] == 'admin':
                if password == ADMIN_PASSWORD:
                    return redirect(url_for('admin.dashboard'))
                else:
                    return render_template('login.html', error="Acceso no autorizado")
            else:
                return redirect(url_for('user.dashboard'))
        else:
            return render_template('login.html', error="Número no registrado")

    return render_template('login.html')
# ===================================================================================================
    