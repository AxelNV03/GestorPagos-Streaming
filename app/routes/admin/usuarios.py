from flask import render_template
from . import admin_bp
from app.utils.decorators import admin_required
# from app.services import (
# 
# )

@admin_bp.route('/usuarios')
@admin_required
def usuarios():
    # 'q' y 'plataforma_id' vienen de los filtros de búsqueda
    # query = request.args.get('q', '')
    # p_id = request.args.get('plataforma_id', '')

    # Por ahora mandamos listas vacías para asegurar la arquitectura
    datos = {
        'usuarios': [],    # Lista vacía para el {% for u in data.usuarios %}
        'listaP': [],      # Lista vacía para el selector de filtros
        # 'filtros': {       # Guardamos los filtros para que no se borren del input
        #     'q': 0,
        #     'p_id': 0
        # }
    }
    
    return render_template('admin/usuarios.html', data=datos)