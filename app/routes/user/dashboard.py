# app/routes/user/dashboard.py
# ===================================================================================================
from flask import render_template, session, g
from . import user_bp
from app.utils.decorators import login_required, user_required
from app.services import PlataformaUsuarioService, CobroService, PeriodoService
from datetime import datetime
# ===================================================================================================
@user_bp.route('/dashboard')
@login_required  # <-- ¡Así de fácil!
def dashboard():
    return render_template('user/dashboard.html')