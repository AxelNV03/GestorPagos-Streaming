from functools import wraps
from flask import session, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_rol') != 'admin':
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function