# app/routes/admin/dashboard.py
# ===================================================================================================
from flask import render_template
from . import admin_bp
from app.utils.decorators import admin_required

from app.services.periodo import PeriodoService
from app.services.plataforma import PlataformaService
# ===================================================================================================
@admin_bp.route('/dashboard')
@admin_required
def index():

    per = PeriodoService.periodo_actual()

    datos = {
        'periodo' : per,
        'pendientes': PlataformaService.pendientes_periodo(per.id)
    }


    # 3. Renderizamos la página principal del admin
    return render_template('admin/admin2.html',**datos)
