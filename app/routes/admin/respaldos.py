# app/routes/admin/respaldos.py
# ===================================================================================================
from . import admin_bp
from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from app.services.backup_service import BackupService
from app.utils.decorators import admin_required
import os
# ===================================================================================================
@admin_bp.route('/respaldos')
@admin_required
def respaldos():
    backups = BackupService.listar_backups()
    return render_template('admin/respaldos/index.html', backups=backups)
# ===================================================================================================
@admin_bp.route('/respaldos/generar', methods=['POST'])
@admin_required
def generar_backup():
    nombre = request.form.get('nombre', '').strip()
    try:
        nombre_backup = BackupService.generar_backup(nombre if nombre else None)
        flash(f'✅ Backup generado: {nombre_backup}', 'success')
    except Exception as e:
        flash(f'Error al generar backup: {str(e)}', 'danger')
    return redirect(url_for('admin.respaldos'))# ===================================================================================================
@admin_bp.route('/respaldos/descargar/<nombre>')
@admin_required
def descargar_backup(nombre):
    ruta = os.path.join(current_app.config['BACKUP_FOLDER'], nombre)
    return send_file(ruta, as_attachment=True)
# ===================================================================================================
@admin_bp.route('/respaldos/eliminar/<nombre>', methods=['POST'])
@admin_required
def eliminar_backup(nombre):
    try:
        BackupService.eliminar_backup(nombre)
        flash('Backup eliminado', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin.respaldos'))
# ===================================================================================================
@admin_bp.route('/respaldos/restaurar', methods=['POST'])
@admin_required
def restaurar_backup():
    archivo = request.files.get('backup_file')
    if not archivo or archivo.filename == '':
        flash('Selecciona un archivo', 'danger')
        return redirect(url_for('admin.respaldos'))
    
    try:
        BackupService.restaurar_backup(archivo)
        flash('✅ Base de datos restaurada correctamente', 'success')
    except Exception as e:
        flash(f'Error al restaurar: {str(e)}', 'danger')
    return redirect(url_for('admin.respaldos'))
# ===================================================================================================
@admin_bp.route('/respaldos/restaurar/<nombre>', methods=['POST'])
@admin_required
def restaurar_backup_archivo(nombre):
    try:
        BackupService.restaurar_desde_archivo(nombre)
        flash('✅ Base de datos restaurada correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin.respaldos'))
# ===================================================================================================