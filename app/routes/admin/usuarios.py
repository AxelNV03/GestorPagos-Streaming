# app/routes/admin/usuarios.py
# ===================================================================================================
from flask import render_template, request, redirect, url_for, flash
from app import db
from . import admin_bp
from app.utils.decorators import admin_required

from app.services.admin_service import AdminService
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
@admin_bp.route('/usuarios')
def usuarios():
    filtros = {
        'query': request.args.get('query', ''),
        'plataforma_id': request.args.get('plataforma_id', '')
    }
    return render_template('admin/usuarios/index.html', **AdminService.panel_usuarios(filtros))
# ===================================================================================================
@admin_bp.route('/usuarios/guardar', methods=['POST'])
@admin_required
def guardar_usuario():
    usuario_id = request.form.get('usuario_id')
    plats_raw = request.form.getlist('plataformas[]')    
    plats_pars = [int(p_id) for p_id in plats_raw if p_id.isdigit()]
    datos = {
        'nombres' : request.form.get('nombres'),
        'apeP' : request.form.get('apeP'),
        'apeM' : request.form.get('apeM'),
        'telefono' : request.form.get('telefono'),
        'correo' : request.form.get('correo'),
        'plataformas' : plats_pars
    }
    
    try:
        AdminService.guardar_usuario(usuario_id, datos)
        flash('¡Usuario guardado exitosamente!', 'success')        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar el usuario: {str(e)}', 'danger')       
    
    return redirect(url_for('admin.usuarios'))