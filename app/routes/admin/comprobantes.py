# app/routes/admin/comprobantes.py
# ===================================================================================================
from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from app.services.admin_service import AdminService
from app.services.periodo_service import PeriodoService
from flask import send_file
import os
from flask import current_app
from app import db
from app.core.models.comprobante import Comprobante
# ===================================================================================================
@admin_bp.route('/comprobantes')
def comprobantes():
    info_p = PeriodoService.obtener_periodo_actual()
    filtros = {
        'estado': request.args.get('estado', ''),
        'mes': request.args.get('mes') or info_p['mes'],
        'anio': request.args.get('anio') or info_p['anio']
    }
    return render_template('admin/comprobantes/index.html', **AdminService.panel_comprobantes(filtros))
# ===================================================================================================
@admin_bp.route('/comprobantes/subir', methods=['POST'])
def subir_comprobante():
    try:
        AdminService.subir_comprobante(
            usuario_id=request.form.get('usuario_id'),
            archivo=request.files.get('archivo'),
            nota=request.form.get('nota', '')
        )
        flash('Comprobante subido correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('admin.comprobantes'))
# ===================================================================================================
@admin_bp.route('/comprobantes/imagen/<int:comprobante_id>')
def ver_imagen(comprobante_id):
    comprobante = db.session.get(Comprobante, comprobante_id)
    if not comprobante:
        return "No encontrado", 404
    
    ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], comprobante.ruta_archivo)
    return send_file(ruta)