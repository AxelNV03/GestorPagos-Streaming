from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Verifica que el usuario haya iniciado sesión"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Por favor, inicia sesión para acceder.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_rol') != 'admin':
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        # Ajustado a tu Enum: 'no_admin'
        if session.get('user_rol') != 'no_admin':
            # Si un admin intenta entrar aquí, lo mandamos a su panel
            return redirect(url_for('admin.index'))
            
        return f(*args, **kwargs)
    return decorated_function