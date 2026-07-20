# app/routes/admin/comprobantes.py
# ===================================================================================================
from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from app.services.admin_service import AdminService
from app.services.periodo_service import PeriodoService
from flask import send_file
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
    try:
        ruta = AdminService.obtener_ruta_imagen(comprobante_id)
        return send_file(ruta)
    except Exception as e:
        return str(e), 404
# ===================================================================================================
@admin_bp.route('/comprobantes/aprobar/<int:comprobante_id>', methods=['POST'])
def aprobar_comprobante(comprobante_id):
    try:
        AdminService.aprobar_comprobante(comprobante_id, request.form)
        flash('Comprobante aprobado correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('admin.comprobantes'))
# ===================================================================================================
@admin_bp.route('/comprobantes/rechazar/<int:comprobante_id>', methods=['POST'])
def rechazar_comprobante(comprobante_id):
    comentario = request.form.get('comentario', '')
    try:
        AdminService.rechazar_comprobante(comprobante_id, comentario)
        flash('Comprobante rechazado correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('admin.comprobantes'))
# ===================================================================================================
