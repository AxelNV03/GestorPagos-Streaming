# app/routes/admin/dashboard.py
# ===================================================================================================
from flask import render_template, request, flash, redirect, url_for
from . import admin_bp
from app.utils.decorators import admin_required

from app.services.admin_service import AdminService
from app.services.periodo_service import PeriodoService
from app.services.plataforma_service import PlataformaService
# ===================================================================================================
@admin_bp.route('/dashboard')
@admin_required
def index():
    return render_template('admin/dashboard.html', **AdminService.dashboard_data())
# ===================================================================================================
# Ruta limpia
@admin_bp.route('/anuncios', methods=['GET', 'POST'])
@admin_required
def anuncios():
    if request.method == 'POST':
        mensaje = request.form.get('mensaje', '')
        enviados = AdminService.enviar_anuncio(mensaje)
        flash(f'Anuncio enviado a {enviados} usuarios', 'success')
        return redirect(url_for('admin.anuncios'))
    
    return render_template('admin/anuncios/index.html')