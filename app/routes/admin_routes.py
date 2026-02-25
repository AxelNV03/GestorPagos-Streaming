# app/routes/admin.py
# ===================================================================================================
from flask import Blueprint, render_template, session, redirect, url_for, g, current_app, request, flash, send_from_directory
from functools import wraps
from collections import defaultdict
from datetime import datetime
from app.services import PlataformaService, UserService, PeriodoService, CobroService, ComprobanteService
# ===================================================================================================
# ===================================================================================================
# El decorador "Guardián"
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_rol') != 'admin':
            return redirect(url_for('main.login')) # Asegúrate que tu login esté en main_bp
        return f(*args, **kwargs)
    return decorated_function
# ===================================================================================================
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
# ===================================================================================================
@admin_bp.before_request
def setup_services():
    # Instanciamos una sola vez por petición
    # g.db debe estar disponible o usas current_app.db
    g.plat = PlataformaService()
    g.per = PeriodoService()
    g.cobros = CobroService()
    g.users = UserService()
    g.comp = ComprobanteService()
# ===================================================================================================
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    periodoActual = g.per.periodo_actual()
    pid, mes, anio = periodoActual['id'], periodoActual['mes'], periodoActual['anio']

    datos = {
        'finanzas_plataformas' : g.plat.recaudacion_plataformas(mes, anio),
        'plataformas_restantes': g.plat.plataformas_restantes_mes(mes, anio),
        'recaudacion' : g.cobros.recaudacion_global(pid),
        'periodo' : periodoActual,
        'cobros_pendientes' : g.cobros.obtener_cobros(switch='revision')
    }

    return render_template('admin/main_page.html', data=datos)
# ===================================================================================================
# ===================================================================================================





# ===================================================================================================
# SERVICIOS
# ===================================================================================================
@admin_bp.route('/servicios')
@admin_required
def servicios():
    periodoActual = g.per.periodo_actual()
    pid, mes, anio = periodoActual['id'], periodoActual['mes'], periodoActual['anio']
    
    datos = {
        'finanzas_plataformas' : g.plat.recaudacion_plataformas(mes, anio),
        'recaudacion' : g.cobros.recaudacion_global(pid),
        'periodo' : periodoActual,
        'conteo_global': g.cobros.conteo_global_users_pagos(pid)
    }
    # Tu código del dashboard
    return render_template('admin/servicios.html', data=datos)
# ===================================================================================================
@admin_bp.route('/servicios/guardar', methods=['POST'])
@admin_required
def guardar_servicio():
    p_id = request.form.get('plataforma_id')
    datos = {
        'nombre' : request.form.get('nombre'),
        'precio_mensual': float(request.form.get('precio_mensual', 0)),
        'dia_cobro': int(request.form.get('dia_cobro', 1)),
        'correo_asociado': request.form.get('correo_asociado'),
        'url_plataforma': request.form.get('url_plataforma'),
        'url_logo': request.form.get('url_logo')
    }

    try:
        # MODO EDICIÓN
        if p_id and p_id.strip():
            res = g.plat.actualizar_plataforma(p_id, datos)   

            if res:
                aux = g.plat.datos_plataforma(p_id)

                # Usamos 'or 0' por si la DB no retorna el conteo de filas
                filas_actualizadas = g.cobros.actualizar_cobros_pendientes_plataforma(
                    p_id, datos['precio_mensual'], aux['total_users']
                ) or 0
                
                msg = f"¡{datos['nombre']} actualizado!"
                if filas_actualizadas > 0:
                    msg += f" Se ajustaron {filas_actualizadas} cobros pendientes."
                
                flash(msg, "success")
            else:
                # Si res es False, puede ser porque no hubo cambios en los datos
                flash(f"No se detectaron cambios en {datos['nombre']}", "info")
        
        # MODO CREACIÓN
        else:
            res = g.plat.crear_plataforma(datos)
            if res:
                flash(f"¡{datos['nombre']} creada correctamente!", "success")
            else:
                flash("No se pudo crear la plataforma", "danger")

    except Exception as e:
        flash(f"Error en la operación: {str(e)}", "danger")


    return redirect(url_for('admin.servicios'))
# ===================================================================================================
@admin_bp.route('/servicios/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar_servicio(id):
    res = g.plat.eliminar_plataforma(id)
    if res:
        flash("Servicio eliminado con éxito.", "success")
    else:
        flash("No se pudo eliminar el servicio.", "error")
    return redirect(url_for('admin.servicios'))
# ===================================================================================================
# ===================================================================================================





# ===================================================================================================
# USUARIOS
# ===================================================================================================
@admin_bp.route('/usuarios')
@admin_required
def usuarios():
    # 'q' y 'plataforma_id' vienen del 'name' de tus inputs en el HTML
    query = request.args.get('q', '')
    p_id = request.args.get('plataforma_id', '')

    datos = {
        'usuarios' : g.users.obtener_usuarios(search_query=query, plataforma_id=p_id),
        'listaP' : g.plat.lista_plataformas()
    }
    return render_template('admin/usuarios.html', data=datos)
# ===================================================================================================
@admin_bp.route('/usuarios/guardar', methods=['POST'])
@admin_required
def guardar_usuario():
    user_id = request.form.get('user_id')
    datos = {
        'nombres' : request.form.get('nombres'),
        'apeP' : request.form.get('apeP'),
        'apeM' : request.form.get('apeM'),
        'telefono' : request.form.get('telefono'),
        'plataforma_id' : request.form.get('plataforma_id')
    }


    try:
        # EDITAR
        if user_id and user_id.strip():
            res = g.users.actualizar_usuario(user_id, datos)
            
            if res is not None:
                flash(f"¡{datos['nombres']} actualizado con éxito!", "success")
            else:
                flash("Error al intentar actualizar el usuario.", "danger")
        # CREAR    
        else:
            nuevo_id = g.users.crear_usuario(datos)

            if nuevo_id:
                pu_id = g.plat.vincular_user_plataforma(nuevo_id, datos['plataforma_id'])
                datos_p = g.plat.datos_plataforma(datos['plataforma_id'])
                periodo = g.per.periodo_actual()
                monto = round(float(datos_p['precio_mensual'])/float(datos_p['total_users']), 2)

                # crea el primer cobro
                g.cobros.crear_cobro(periodo['id'], pu_id, monto)

                # Actualiza los pagos
                actu = g.cobros.actualizar_cobros_pendientes_plataforma(
                    datos_p['id'],
                    datos_p['precio_mensual'],
                    datos_p['total_users']
                )

                flash(f"Usuario creado. Primer pago generado.", "success")
            else:
                return False
    except Exception as e:
        flash(f"Error en la operación: {str(e)}", "danger")

    return redirect(url_for('admin.usuarios'))
# ===================================================================================================
@admin_bp.route('/usuarios/eliminar/<int:id>/<int:plat_id>', methods=['POST'])
@admin_required
def eliminar_usuario(id, plat_id):
    try:
        # 1. Borramos al usuario (la DB limpia vínculos y cobros por CASCADE)
        res = g.users.eliminar_usuario(id)
        
        if res:
            # 2. Recalculamos usando el plat_id que vino directo de la URL
            datos_p = g.plat.datos_plataforma(plat_id)
            
            if datos_p:
                # Actualizamos los montos de los cobros pendientes
                actu = g.cobros.actualizar_cobros_pendientes_plataforma(
                    datos_p['id'],
                    datos_p['precio_mensual'],
                    datos_p['total_users']
                )
                flash(f"Usuario eliminado. Se actualizaron {actu} cobros de la plataforma.", "success")
            else:
                flash("Usuario eliminado, pero no se encontró la plataforma para recalcular.", "warning")
        else:
            flash("No se pudo eliminar el usuario de la base de datos.", "danger")

    except Exception as e:
        flash(f"Error crítico al eliminar: {str(e)}", "danger")
    
    return redirect(url_for('admin.usuarios'))
# ===================================================================================================
# ===================================================================================================






# ===================================================================================================
# COBROS
# ===================================================================================================
@admin_bp.route('/cobros')
@admin_required
def cobros():
    # Datos de periodo actual
    periodoActual = g.per.periodo_actual()
    pid, mes, anio = periodoActual['id'], periodoActual['mes'], periodoActual['anio']

    #Datos de filtros
    q = request.args.get('q', '')
    mes = request.args.get('mes', '')
    anio = request.args.get('anio', anio)
    plat_id = request.args.get('plataforma_id', '')

    # Consulta
    resultados = g.cobros.obtener_cobros(
        busqueda=q, 
        mes=mes, 
        anio=anio, 
        plataforma=plat_id
    )

    # Agrupamos por meses
    cobros_agrupados = defaultdict(list)
    for cobro in (resultados or []):
        # Usamos el nombre del mes que ya inyectamos en el modelo
        mes_anio = f"{cobro['nombre_mes']} {cobro['anio']}"
        cobros_agrupados[mes_anio].append(cobro)
    
    datos = {
        'finanzas_plataformas': g.plat.recaudacion_plataformas(mes, anio),
        'recaudacion': g.cobros.recaudacion_global(pid), # O usar el pid filtrado si lo calculas
        'periodo': periodoActual,
        'plats' : g.plat.lista_plataformas(),
        'conteo_global': g.cobros.conteo_global_users_pagos(pid),
        'cobros_lista': cobros_agrupados,
        'filtros': { 'q': q, 'mes': mes, 'anio': int(anio), 'plat_id': plat_id },
        'hoy' : datetime.now().date() # Enviamos el objeto fecha real
    }

    return render_template('admin/cobros.html', data=datos)
# ===================================================================================================
@admin_bp.route('/pago/<string:accion>/<int:pago_id>', methods=['POST'])
@admin_required
def gestionar_pago(accion, pago_id):
    meses = int(request.form.get('meses', 1))
    data_cobro = g.cobros.obtener_cobro(pago_id)
    periodoCobro = data_cobro['periodo_id']

    try:
        if accion == 'aprobar':
            # 1. Actualizar registros existentes
            g.comp.actualizar_comprobante('aprobado', data_cobro['comprobante_id'])
            g.cobros.actualizar_cobro('pagado', pago_id)

            # 2. Crear cobros adelantados (si meses > 1)
            for i in range(1, meses):
                nuevo_id = g.cobros.crear_cobro(periodoCobro + i, data_cobro['user_plataforma_id'], data_cobro['monto'])
                g.cobros.asociar_comprobante(data_cobro['comprobante_id'], nuevo_id)
                g.cobros.actualizar_cobro('pagado', nuevo_id)

            # 3. Siguiente pendiente
            g.cobros.crear_cobro(periodoCobro + meses, data_cobro['user_plataforma_id'], data_cobro['monto'])
            
            flash("✅ Pago aprobado y periodos actualizados", "success")

        else:
            # Lógica de rechazo...
            g.comp.actualizar_comprobante('rechazado', data_cobro['comprobante_id'])
            g.cobros.actualizar_cobro('rechazado', pago_id)
            g.cobros.crear_cobro(periodoCobro, data_cobro['user_plataforma_id'], data_cobro['monto'])
            
            flash("❌ Comprobante rechazado", "warning")

        # --- EL COMMIT VA AQUÍ ---
        # Una vez que todas las funciones de arriba terminaron sin error

    except Exception as e:
        # Si algo falló en cualquier punto del try, deshacemos todo
        print(f"Error procesando pago: {str(e)}")
        flash(f"🔥 Error crítico: {str(e)}", "danger")

    return redirect(request.referrer or url_for('admin.cobros'))
# ===================================================================================================
# ===================================================================================================





# ===================================================================================================
# COMPROBANTES
# ===================================================================================================
@admin_bp.route('/cobros/subir_comprobante', methods=['POST'])
@admin_required
def subir_comprobante():
    # 1. Datos del formulario
    id_cobro = request.form.get('id_cobro')
    user_id = request.form.get('usuario_id')
    nota = request.form.get('nota', '')
    archivo = request.files.get('comprobante')

    # Validación de seguridad básica
    if not archivo or not user_id:
        flash("Datos incompletos. Intenta de nuevo.", "danger")
        return redirect(url_for('admin.cobros'))

   # Llamamos a tu función y capturamos la ruta generada
    try:
        path_file = g.comp.save_file(archivo, user_id)
        comp_id = g.comp.crear_registro(path_file, nota)
        g.cobros.asociar_comprobante(comp_id, id_cobro)
        # DEBUG MAESTRO: Aquí vemos todo el viaje de los datos
        flash("✅ Comprobante adjuntado.", "success")        
    except Exception as e:
        flash(f"🔥 Error al procesar registro: {str(e)}", "danger")
    return redirect(url_for('admin.cobros'))    
    # return render_template('admin/cobros.html')
# ===================================================================================================
@admin_bp.route('/comprobante/archivo/<path:filename>') # <--- Esta parte debe ser igual
@admin_required
def servir_comprobante(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
# ===================================================================================================
# ===================================================================================================