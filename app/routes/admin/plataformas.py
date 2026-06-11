# app/routes/admin/plataformas.py
# ===================================================================================================
from flask import Blueprint, request, redirect, url_for, flash, current_app, render_template
from app import db
from . import admin_bp
from app.utils.decorators import admin_required
from werkzeug.utils import secure_filename

from app.services.admin_service import AdminService
from app.services.plataforma_service import PlataformaService
# ===================================================================================================
@admin_bp.route('/plataformas')
@admin_required
def plataformas():
    return render_template('admin/plataformas/index.html', **AdminService.panel_plataformas())
# ===================================================================================================
@admin_bp.route('/plataformas/guardar', methods=['POST'])
@admin_required
def guardar_plataforma():
    plataforma_id = request.form.get('plataforma_id')
    archivo_logo = request.files.get('logo')
    datos = {
        'nombre': request.form.get('nombre', ''),
        'precio_total': float(request.form.get('precio_total', 0.00)),
        'dia_cobro': int(request.form.get('dia_cobro', 1)),
        'cuota': float(request.form.get('cuota', 0.00)),
        'correo_admin': request.form.get('correo_admin')
    }
    try:
        AdminService.guardar_plataforma(plataforma_id, datos, archivo_logo)    
        flash('¡Plataforma guardada exitosamente!', 'success') 
    except Exception as e:
        flash(f'Error al guardar la plataforma: {str(e)}', 'danger') 

    return redirect(url_for('admin.plataformas'))
# ===================================================================================================
@admin_bp.route('/plataformas/eliminar/<int:p_id>', methods=['POST'])
@admin_required
def eliminar_plataforma(p_id):
    try:
        # La ruta solo da la orden y confía en el servicio
        AdminService.borrar_plataforma(p_id)
        flash("¡Plataforma eliminada correctamente!", "success")
    except Exception as e:
        # El rollback ya ocurrió adentro, aquí solo avisamos y redirigimos
        flash(f"No se pudo eliminar la plataforma: {str(e)}", "danger")
        
    return redirect(url_for('admin.plataformas'))
# ===================================================================================================
