# app/routes/admin/cobros.py
# ===================================================================================================
from . import admin_bp
from flask import render_template, request
from app.services.admin_service import AdminService
# ===================================================================================================
@admin_bp.route('/cobros')
def cobros():
    filtros = {
        'query': request.args.get('query', ''),
        'plataforma_id': request.args.get('plataforma_id', ''),
        'mes': request.args.get('mes', ''),
        'anio': request.args.get('anio', '')
    }
    return render_template('admin/cobros/index.html', **AdminService.panel_cobros(filtros))



