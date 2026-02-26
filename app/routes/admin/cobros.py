from flask import render_template, request
from . import admin_bp
from app.utils.decorators import admin_required
from datetime import datetime
# from app.services import (
# 
# )

# @admin_bp.route('/cobros')
# @admin_required
# def cobros():
#     # Datos de periodo actual
#     periodoActual = g.per.periodo_actual()
#     pid, mes, anio = periodoActual['id'], periodoActual['mes'], periodoActual['anio']

#     #Datos de filtros
#     q = request.args.get('q', '')
#     mes = request.args.get('mes', '')
#     anio = request.args.get('anio', anio)
#     plat_id = request.args.get('plataforma_id', '')

#     # Consulta
#     resultados = g.cobros.obtener_cobros(
#         busqueda=q, 
#         mes=mes, 
#         anio=anio, 
#         plataforma=plat_id
#     )

#     # Agrupamos por meses
#     cobros_agrupados = defaultdict(list)
#     for cobro in (resultados or []):
#         # Usamos el nombre del mes que ya inyectamos en el modelo
#         mes_anio = f"{cobro['nombre_mes']} {cobro['anio']}"
#         cobros_agrupados[mes_anio].append(cobro)
    
#     datos = {
#         'finanzas_plataformas': g.plat.recaudacion_plataformas(mes, anio),
#         'recaudacion': g.cobros.recaudacion_global(pid), # O usar el pid filtrado si lo calculas
#         'periodo': periodoActual,
#         'plats' : g.plat.lista_plataformas(),
#         'conteo_global': g.cobros.conteo_global_users_pagos(pid),
#         'cobros_lista': cobros_agrupados,
#         'filtros': { 'q': q, 'mes': mes, 'anio': int(anio), 'plat_id': plat_id },
#         'hoy' : datetime.now().date() # Enviamos el objeto fecha real
#     }

#     return render_template('admin/cobros.html', data=datos)


@admin_bp.route('/cobros')
@admin_required
def cobros():
    # 1. Definimos el periodo vacío (para que el header no rompa)
    periodo_vacio = {
        'id': 0, 
        'mes': 0, 
        'anio': 2026, 
        'nombre_mes': 'Sin Periodo'
    }

    # 2. Captura de filtros (aunque no busquen nada aún)
    q = request.args.get('q', '')
    f_mes = request.args.get('mes', '')
    f_anio = request.args.get('anio', '2026')
    plat_id = request.args.get('plataforma_id', '')

    # 3. Diccionario de datos con listas y diccionarios vacíos
    datos = {
        'finanzas_plataformas': [],
        'recaudacion': {
            'recaudado': 0.0, 
            'pendiente': 0.0
        },
        'periodo': periodo_vacio,
        'plats': [],
        'conteo_global': {
            'pagos': 0, 
            'users': 0
        },
        'cobros_lista': {}, # Diccionario vacío para el agrupamiento
        'filtros': { 
            'q': q, 
            'mes': f_mes, 
            'anio': f_anio, 
            'plat_id': plat_id 
        },
        'hoy': datetime.now().date()
    }

    return render_template('admin/cobros.html', data=datos)

@admin_bp.route('/cobros/cargar')
@admin_required
def subir_comprobante():
        return True