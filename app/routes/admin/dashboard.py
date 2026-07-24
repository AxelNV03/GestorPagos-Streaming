# app/routes/admin/dashboard.py
# ===================================================================================================
from flask import request, flash, redirect, url_for, render_template
from . import admin_bp
from app.utils.decorators import admin_required

from app.services.admin_service import AdminService
# ===================================================================================================
@admin_bp.route('/dashboard')
@admin_required
def index():
    return render_template('admin/dashboard.html', **AdminService.dashboard_data())
# ===================================================================================================
@admin_bp.route('/anuncios/enviar', methods=['POST'])
@admin_required
def enviar_anuncio():
    alcance = request.form.get('alcance')
    mensaje = request.form.get('mensaje', '')
    
    if alcance == 'plataforma':
        plataforma_id = request.form.get('plataforma_id')
        enviados = AdminService.enviar_anuncio_plataforma(plataforma_id, mensaje)
    else:
        usuarios_ids = request.form.getlist('usuarios_ids')
        enviados = AdminService.enviar_anuncio_usuarios(usuarios_ids, mensaje)
    
    flash(f'Anuncio enviado a {enviados} usuarios', 'success')
    return redirect(url_for('admin.index'))
# ===================================================================================================
