# app/routes/user/dashboard.py
# ===================================================================================================
from flask import render_template, session, g
from . import user_bp
from app.utils.decorators import login_required, user_required
from app.services import PlataformaUsuarioService, CobroService, PeriodoService
from datetime import datetime
# ===================================================================================================
@user_bp.route('/dashboard')
@login_required  # <-- ¡Así de fácil!
def dashboard():
    return render_template('user/dashboard.html')

#  def dashboard():
#     u_id = session.get('user_id')
#     cobro = g.cobros.ultimo_cobro(u_id, 'pendiente')
#     per_act = g.per.periodo_actual()
#     clase_pago = "" 
    
#     if cobro and cobro['limite_pago']:
#         # 1. Aseguramos que 'hoy' y 'fecha_limite' sean solo fecha (sin horas)
#         hoy = datetime.now().date()
#         fecha_limite = cobro['limite_pago']
        
#         # Si viene de la DB como datetime, lo pasamos a date
#         if hasattr(fecha_limite, 'date'):
#             fecha_limite = fecha_limite.date()

#         # 1. Prioridad: Esta al corriente

#         delta = fecha_limite - hoy
#         # Guardamos el número de días (puede ser negativo si ya pasó)
#         cobro['dias_restantes'] = delta.days
#         dias_r = cobro.get('dias_restantes')
        
#         # 1. PRIORIDAD MÁXIMA: Si ya subió comprobante, ignoramos todo lo demás
#         if cobro.get('comprobante_id') is not None:
#             clase_pago = "pago-revision" # Azul
#         # 2. SEGUNDA PRIORIDAD: Si ya pasó la fecha (Vencido)
#         elif hoy > fecha_limite:
#             clase_pago = "pago-vencido"  # Rojo
#         # 3. TERCERA PRIORIDAD: Si es hoy o faltan 5 días o menos (Urgente/Naranja)
#         elif hoy == fecha_limite or (0 <= dias_r <= 5):
#             clase_pago = "pago-hoy"      # Naranja
#         # 4. CASO BASE: Todo está bien y falta más de una semana
#         else:
#             clase_pago = "pago-normal"   # Gris/Verde (Al corriente)

#     datos = {
#         'periodo' : per_act,
#         'user' : g.users.buscar_usuario(user_id=u_id),
#         'last_p' : cobro,
#         'clase_pago': clase_pago
#     }

#     return render_template('user/dashboard.html', data=datos)