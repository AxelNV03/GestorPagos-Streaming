# app/routes/user/dashboard.py
# ===================================================================================================
from flask import render_template, session, g, request
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
    mes = request.args.get('mes')
    anio = request.args.get('anio')
    return render_template('user/historial.html', data=NoAdminService.historial_data(mes, anio))

# app/routes/user/dashboard.py
@user_bp.route('/historial/<int:id>')
@login_required
def ver_recibo(id):
    data = NoAdminService.ver_recibo_data(id)
    return render_template('user/ver_recibo.html', data=data)

@user_bp.route('/pago')
@login_required
def seccion_comprobante():
    return render_template('user/subir_pago.html')