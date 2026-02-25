# app/routes/user_routes.py
# ===================================================================================================
from flask import Blueprint, render_template, session, redirect, url_for, g, current_app, request, flash, send_from_directory
from app.services import PlataformaService, UserService, PeriodoService, CobroService, ComprobanteService
from datetime import datetime
from functools import wraps
# ===================================================================================================
# ===================================================================================================
user_bp = Blueprint('user', __name__, url_prefix='/user')
# ===================================================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si la sesión no tiene el user_id, lo mandamos al login
        if 'user_id' not in session:
            flash("Por favor, inicia sesión para acceder.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
# ===================================================================================================
@user_bp.before_request
def setup_services():
    # Instanciamos una sola vez por petición
    # g.db debe estar disponible o usas current_app.db
    g.plat = PlataformaService()
    g.per = PeriodoService()
    g.cobros = CobroService()
    g.users = UserService()
    g.comp = ComprobanteService()
# ===================================================================================================
@user_bp.route('/dashboard')
@login_required  # <-- ¡Así de fácil!
def dashboard():
    u_id = session.get('user_id')
    cobro = g.cobros.ultimo_cobro(u_id, 'pendiente')
    per_act = g.per.periodo_actual()
    clase_pago = "" 
    
    if cobro and cobro['limite_pago']:
        # 1. Aseguramos que 'hoy' y 'fecha_limite' sean solo fecha (sin horas)
        hoy = datetime.now().date()
        fecha_limite = cobro['limite_pago']
        
        # Si viene de la DB como datetime, lo pasamos a date
        if hasattr(fecha_limite, 'date'):
            fecha_limite = fecha_limite.date()

        # 1. Prioridad: Esta al corriente

        delta = fecha_limite - hoy
        # Guardamos el número de días (puede ser negativo si ya pasó)
        cobro['dias_restantes'] = delta.days
        dias_r = cobro.get('dias_restantes')
        
        # 1. PRIORIDAD MÁXIMA: Si ya subió comprobante, ignoramos todo lo demás
        if cobro.get('comprobante_id') is not None:
            clase_pago = "pago-revision" # Azul
        # 2. SEGUNDA PRIORIDAD: Si ya pasó la fecha (Vencido)
        elif hoy > fecha_limite:
            clase_pago = "pago-vencido"  # Rojo
        # 3. TERCERA PRIORIDAD: Si es hoy o faltan 5 días o menos (Urgente/Naranja)
        elif hoy == fecha_limite or (0 <= dias_r <= 5):
            clase_pago = "pago-hoy"      # Naranja
        # 4. CASO BASE: Todo está bien y falta más de una semana
        else:
            clase_pago = "pago-normal"   # Gris/Verde (Al corriente)

    datos = {
        'periodo' : per_act,
        'user' : g.users.buscar_usuario(user_id=u_id),
        'last_p' : cobro,
        'clase_pago': clase_pago
    }

    return render_template('user/dashboard.html', data=datos)
# ===================================================================================================
@user_bp.route('/pago')
@login_required  # <-- ¡Así de fácil!
def seccion_comprobante():
    return render_template('user/subir_pago.html')
# ===================================================================================================
@user_bp.route('/logout')
def logout():
    # Limpiamos toda la información de la sesión
    session.clear()
    # Redirigimos al login (ajusta 'main.login' si tu ruta de entrada es distinta)
    return redirect(url_for('main.login'))
# ===================================================================================================
@user_bp.route('/pago/comprobante', methods=['POST'])
@login_required  # <-- ¡Así de fácil!
def subir_comprobante():
    u_id = session.get('user_id')
    data_cobro = g.cobros.ultimo_cobro(u_id, 'pendiente')
    id_cobro = data_cobro['id']
    nota = request.form.get('notas')
    archivo = request.files.get('comprobante')


    # Validación de seguridad básica
    if not archivo or not u_id:
        flash("Datos incompletos. Intenta de nuevo.", "danger")
        return redirect(url_for('user.seccion_comprobante'))
    
    if not nota or not nota.strip():
        nota = "Ninguna"
    
   # Llamamos a tu función y capturamos la ruta generada
    try:
        path_file = g.comp.save_file(archivo, u_id)
        comp_id = g.comp.crear_registro(path_file, nota)
        g.cobros.asociar_comprobante(comp_id, id_cobro)
        # DEBUG MAESTRO: Aquí vemos todo el viaje de los datos
        flash("✅ Comprobante enviado. Puedes volver al menu principal", "success")        
    except Exception as e:
        flash(f"🔥 Error al procesar registro: {str(e)}", "danger")

    return redirect(url_for('user.seccion_comprobante'))    

# ===================================================================================================
@user_bp.route('/historial')
@login_required  # <-- ¡Así de fácil!
def historial():
    u_id = session.get('user_id')
    
    datos = {
        'pagos': g.cobros.historial_user(u_id)
    }
    return render_template('user/historial.html', data=datos)
# ===================================================================================================
@user_bp.route('/historial/<int:id>')
def ver_recibo(id):
    pago = g.cobros.obtener_cobro(id)
    return render_template('user/ver_recibo.html', pago=pago)
# ===================================================================================================
@user_bp.route('/comprobante/archivo/<path:filename>')
@login_required # O la protección que uses para usuarios
def servir_comprobante_user(filename):
    # Esto busca el archivo en la misma carpeta que usa el admin
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
# ===================================================================================================
