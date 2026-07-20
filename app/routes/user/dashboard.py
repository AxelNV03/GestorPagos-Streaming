# app/routes/user/dashboard.py
# ===================================================================================================
from flask import render_template, session, g
from . import user_bp
from app.utils.decorators import login_required, user_required
from app.services import PlataformaUsuarioService, CobroService, PeriodoService, NoAdminService
from datetime import datetime
# ===================================================================================================
@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html', data=NoAdminService.dashboard_data())
@user_bp.route('/historial')
@login_required
def historial():
    return render_template('user/historial.html')

@user_bp.route('/pago')
@login_required
def seccion_comprobante():
    return render_template('user/subir_pago.html')