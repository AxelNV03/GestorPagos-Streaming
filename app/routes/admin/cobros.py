# app/routes/admin/cobros.py
# ===================================================================================================
from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from app.services.admin_service import AdminService
from app.services.periodo_service import PeriodoService
# ===================================================================================================
@admin_bp.route('/cobros')
def cobros():
    info_p = PeriodoService.obtener_periodo_actual()
    filtros = {
        'query': request.args.get('query', ''),
        'plataforma_id': request.args.get('plataforma_id', ''),
        'mes': request.args.get('mes') or info_p['mes'],
        'estado': request.args.get('estado', ''),  
        'anio': request.args.get('anio') or info_p['anio']
    }
    return render_template('admin/cobros/index.html', **AdminService.panel_cobros(filtros))
# ===================================================================================================
@admin_bp.route('/cobros/cargo-extra', methods=['POST'])
def generar_cargo_extra():
    datos = {
        'alcance' : request.form.get('alcance'),
        'monto' : float(request.form.get('monto', 0)),
        'concepto' : request.form.get('concepto'),
        'usuario_id' : request.form.get('usuario_id'),
        'plataforma_id' : request.form.get('plataforma_id')
    }
    try:
        AdminService.cobro_extra(datos)
        flash('¡Cobro generado exitosamente!', 'success') 
    except Exception as e:
        flash(f'Error al generar el cobro: {str(e)}', 'danger') 

    return redirect(url_for('admin.cobros')) # Regresa al panel
# ===================================================================================================
@admin_bp.route('/cobros/eliminar/<int:cobro_id>', methods=['POST'])
def eliminar_cobro(cobro_id):
    try:
        AdminService.eliminar_cobro(cobro_id)
        flash('Cobro eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el cobro: {str(e)}', 'danger')
    
    return redirect(url_for('admin.cobros'))
# ===================================================================================================
@admin_bp.route('/cobros/editar/<int:cobro_id>', methods=['POST'])
def editar_cobro(cobro_id):
    datos = {
        'motivo': request.form.get('motivo'),
        'monto': float(request.form.get('monto', 0))
    }
    try:
        actualizado = AdminService.editar_cobro(cobro_id, datos)
        if actualizado:
            flash('Cobro actualizado correctamente', 'success')
        else:
            flash('No se realizaron cambios', 'info')
    except Exception as e:
        flash(f'Error al editar el cobro: {str(e)}', 'danger')
    
    return redirect(url_for('admin.cobros'))
# ===================================================================================================