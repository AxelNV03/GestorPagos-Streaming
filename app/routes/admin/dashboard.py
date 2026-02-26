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
