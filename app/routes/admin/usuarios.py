# app/routes/admin/usuarios.py
# ===================================================================================================
from flask import render_template, request, redirect, url_for, flash
from app import db
from . import admin_bp
from app.utils.decorators import admin_required

from app.services.admin_service import AdminService
from app.services.usuario_service import UsuarioService
from app.services.bot_service import BotService

# ===================================================================================================
@admin_bp.route('/usuarios')
def usuarios():
    BotService.notificar_admin("🤖 *Prueba desde GestorPagos*\n\nEl bot está funcionando correctamente. ✅")
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
    plataformas_user = request.form.getlist('plataformas[]')    
    correos_plataforma = request.form.getlist('correos_plataforma[]')
    ids_plataformas_user = [int(p_id) for p_id in plataformas_user if p_id.isdigit()]
    
    datos = {
        'nombres' : request.form.get('nombres'),
        'apeP' : request.form.get('apeP'),
        'apeM' : request.form.get('apeM'),
        'telefono' : request.form.get('telefono'),
        'correo' : request.form.get('correo'),
        'plataformas' : ids_plataformas_user,
        'correos_plataforma': dict(zip(ids_plataformas_user, correos_plataforma))
    }
    
    try:
        AdminService.guardar_usuario(usuario_id, datos)
        flash('¡Usuario guardado correctamente!', 'success')
    except Exception as e:
        flash(f'Error al guardar el usuario: {str(e)}', 'danger')       
    
    return redirect(url_for('admin.usuarios'))
# ===================================================================================================
@admin_bp.route('/usuarios/eliminar/<int:u_id>', methods=['POST'])
@admin_required
def eliminar_usuario(u_id):
    try:
        UsuarioService.eliminar_usuario(u_id)
        flash("¡Usuario eliminado correctamente!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"No se pudo eliminar al usuario: {str(e)}", "danger")
    
    return redirect(url_for('admin.usuarios'))
# ===================================================================================================
@admin_bp.route('/usuarios/<int:usuario_id>')
def detalle_usuario(usuario_id):
    data = AdminService.panel_usuario(usuario_id, request.args)
    return render_template('admin/usuarios/detalle.html', **data)
# ===================================================================================================