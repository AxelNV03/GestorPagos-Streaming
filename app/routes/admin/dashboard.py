# app/routes/admin/dashboard.py
# ===================================================================================================
from flask import render_template
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
# TEST

@admin_bp.route('/usuarios')
def usuarios(): # <--- ESTE NOMBRE es el que busca url_for
    return render_template('admin/dashboard.html')

@admin_bp.route('/cobros')
def cobros(): # <--- ESTE NOMBRE es el que busca url_for
    return render_template('admin/dashboard.html')
