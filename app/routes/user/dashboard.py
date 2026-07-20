# app/routes/user/dashboard.py
# ===================================================================================================
from flask import render_template, session, g, request, flash, redirect, url_for
from flask import send_from_directory, current_app
from . import user_bp
from app.utils.decorators import login_required, user_required
from app.services import PlataformaUsuarioService, CobroService, PeriodoService, NoAdminService
from datetime import datetime
# ===================================================================================================
@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html', data=NoAdminService.dashboard_data())
# ===================================================================================================
@user_bp.route('/historial')
@login_required
def historial():
    mes = request.args.get('mes')
    anio = request.args.get('anio')
    return render_template('user/historial.html', data=NoAdminService.historial_data(mes, anio))
# ===================================================================================================
@user_bp.route('/historial/<int:id>')
@login_required
def ver_recibo(id):
    try:
        data = NoAdminService.ver_recibo_data(id)
        return render_template('user/ver_recibo.html', data=data)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('user.historial'))
# ===================================================================================================
@user_bp.route('/pago')
@login_required
def seccion_comprobante():
    return render_template('user/subir_pago.html')
# ===================================================================================================
@user_bp.route('/comprobante/archivo/<path:filename>')
@login_required
def servir_comprobante_user(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
# ===================================================================================================
@user_bp.route('/comprobante/<int:id>')
@login_required
def ver_comprobante_rechazado(id):
    data = NoAdminService.ver_comprobante_data(id)
    return render_template('user/ver_recibo.html', data=data)