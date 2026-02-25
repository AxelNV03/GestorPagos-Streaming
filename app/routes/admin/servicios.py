from flask import render_template
from . import admin_bp
from app.utils.decorators import admin_required
# from app.services import (
# 
# )

@admin_bp.route('/servicios')
@admin_required
def servicios():
    datos = {
        'finanzas_plataformas': [], # Lista vacía para el {% for %}
        'recaudacion': {
            'recaudado': 0.0,
            'pendiente': 0.0
        },
        'periodo': {
            'nombre_mes': None,    # El filtro |default('Sin Mes') se activará aquí
            'anio': '',            # Se mostrará vacío si no hay dato
            'limite_pago': None    # El filtro |default('No definido') se activará aquí
        },
        'conteo_global': {
            'pagos': 0, # Necesario para la división en el HTML
            'users': 0  # Necesario para el "if users > 0"
        }
    }




    # Tu código del dashboard
    return render_template('admin/servicios.html', data=datos)