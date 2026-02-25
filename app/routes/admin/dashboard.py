from flask import render_template
from . import admin_bp
from app.utils.decorators import admin_required
# from app.services import (
# 
# )

@admin_bp.route('/dashboard')
@admin_required
def index():
    datos = {
        'periodo': {},  # Si esto falta, falla data.periodo.nombre_mes
        'recaudacion': {
            'recaudado': 0,
            'pendiente': 0
        },
        'plataformas_restantes': [],
        'finanzas_plataformas': [],
        'cobros_pendientes': []
    }

    # 3. Renderizamos la página principal del admin
    return render_template('admin/dashboard.html', data=datos)

@admin_bp.route('/usuarios')
@admin_required
def usuarios():
    return "Pantalla de Usuarios (Próximamente)"

@admin_bp.route('/servicios')
@admin_required
def servicios():
    return "Pantalla de Servicios/Plataformas (Próximamente)"

@admin_bp.route('/cobros')
@admin_required
def cobros():
    return "Pantalla de Cobros (Próximamente)"