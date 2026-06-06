# app/services/admin_service.py
# ===================================================================================================
from app.services.usuario_service import UsuarioService
from app.services.plataforma_service import PlataformaService
from app.services.plataforma_usuario_service import PlataformaUsuarioService
from app.services.cobro_service import CobroService
from app.services.periodo_service import PeriodoService
from app.core.models.plataforma import Plataforma
from app.core.models.usuario import Usuario


from app import db
from flask import flash
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
# ===================================================================================================
class AdminService:
    @staticmethod
    def dashboard_data():
        """Recopila toda la info para la pantalla principal"""
        # 1. Obtenemos los datos base (mes, año, label)
        info_p = PeriodoService.obtener_periodo_actual()
        
        # 2. Obtenemos los cálculos financieros (recaudado, restante, esperado)
        finanzas = CobroService.balance_global(info_p['mes'], info_p['anio'])

        # 3. Obtenemos los objetos de plataformas con deudas
        plataformas = PlataformaService.obtener_todas()

        plataformas_deudoras = []
        for p in plataformas:
            # Ejecutamos tus dos funciones especialistas pasándole el ID de la plataforma en turno
            p.finanzas = CobroService.finanzas_plataforma(p.id, info_p["mes"], info_p["anio"])
            p.conteos = CobroService.conteo_pagos_plataforma(p.id, info_p["mes"], info_p["anio"])
            if p.conteos['no_pagados'] > 0:
                plataformas_deudoras.append(p)


        # 3. Construimos un objeto unificado
        return {
            "periodo": {
                "label": info_p['label'],
                "nombre_mes": info_p['nombre_mes'],
                "anio": info_p['anio'],
                "total_recaudado": finanzas['recaudado'],
                "total_restante": finanzas['restante'],
                "total_esperado": finanzas['total_esperado'],
                "tiene_datos": finanzas['tiene_datos']
            },
            "plataformas": plataformas,  # <--- Enviamos la lista aquí
            "plataformas_pendientes": plataformas_deudoras
        }

    @staticmethod
    def panel_plataformas():

        # Datos generales del periodo actual
        info_p = PeriodoService.obtener_periodo_actual()
        finanzas = CobroService.balance_global(info_p['mes'], info_p['anio'])
        conteo_pagos = CobroService.conteo_pagos_periodo(info_p['mes'], info_p['anio'])
        
        # Datos de cada plataforma
        plataformas = PlataformaService.obtener_todas()
        plataformas_info = []
        for p in plataformas:
            # 2. Obtenemos los datos de CobroService para esta plataforma
            finanzasP = CobroService.finanzas_plataforma(p.id, info_p["mes"], info_p["anio"])
            conteos = CobroService.conteo_pagos_plataforma(p.id, info_p["mes"], info_p["anio"])
            
            # 3. Armamos el diccionario mezclando los datos del modelo + los cálculos
            plataformas_info.append({
                "id": p.id,
                "nombre": p.nombre,
                "correo_admin": p.correo_admin,
                "url_logo": p.url_logo,
                "precio_total": p.precio_total,
                "dia_cobro": p.dia_cobro,
                
                # Datos de tus @properties del modelo:
                "cuota": p.cuota,
                "cupos": p.cupos_disponibles,
                "total_usersP": p.total_usuarios,
                
                # Datos financieros que acabas de calcular en tiempo real:
                "recaudado": finanzasP["recaudado"],
                "restante": finanzasP["restante"],
                "pagados": conteos["pagados"],
                "no_pagados": conteos["no_pagados"]
            })


        return {
            'periodo' : info_p['label'],
            'plataformas' : plataformas_info,
            'recaudado' : finanzas['recaudado'],
            'restante' : finanzas['restante'],
            'total_users' : conteo_pagos['users'],
            'pagos_realizados' : conteo_pagos['pagos']
        }

    @staticmethod
    def guardar_plataforma(plataforma_id, datos, archivo_logo):
        if plataforma_id and plataforma_id.strip():
            # Edición
            p = Plataforma.query.get_or_404(plataforma_id)            
            cuota_anterior = float(p.cuota)
            cuota_nueva = float(datos['cuota'])
            
            debe_actualizar_cobros = (cuota_anterior != cuota_nueva)

            # Actualizamos los datos del modelo
            p.nombre = datos['nombre']
            p.precio_total = datos['precio_total']
            p.dia_cobro = datos['dia_cobro']
            p.cuota = datos['cuota'] 
            p.correo_admin = datos['correo_admin']

            p_actualizada = PlataformaService.editar_plataforma(plataforma_id, datos, archivo_logo)

            if debe_actualizar_cobros:
                plataformas_ids = PlataformaUsuarioService.obtener_ids_por_plataforma(p_actualizada.id)
                CobroService.actualizar_monto_cobros(plataformas_ids, p_actualizada.cuota)

            # filas_actualizadas = 0
            # if precio_anterior != precio_nuevo:
            #     # Tu función que ajusta cobros en la DB:
            #     filas_actualizadas = CobroService.actualizar_cobros_pendientes_plataforma(
            #         p.id, precio_nuevo, p.total_usuarios
            #     ) or 0

            # mensaje = f"¡{p.nombre} actualizada correctamente!"
            # if filas_actualizadas > 0:
            #     mensaje += f" Se ajustaron {filas_actualizadas} cobros pendientes."
                
            # tipo_flash = "success"
        else:
            p = PlataformaService.nueva_plataforma(datos, archivo_logo)
            mensaje = f"¡{p.nombre} creada correctamente!"
            tipo_flash = "success"

    @staticmethod
    def borrar_plataforma(p_id):
        """
        Orquesta el borrado físico completo de una plataforma y sus dependencias
        de manera transaccional (Todo o Nada).
        """
        try:
            # 1. Borrar el logo físico del disco antes de perder el registro
            PlataformaService.eliminar_archivo_logo(p_id)

            # 2. Obtener los IDs de los contratos/usuarios asociados
            vinculos_ids = PlataformaUsuarioService.obtener_ids_por_plataforma(p_id)

            # 3. Eliminar los Cobros (Nietos) si existen usuarios asociados
            if vinculos_ids:
                CobroService.borrado_total_por_ids(vinculos_ids)

            # 4. Eliminar los registros de PlataformaUsuario (Hijos)
            PlataformaUsuarioService.eliminar_registros_plataforma(p_id)

            # 5. Eliminar la Plataforma (Padre) de la DB
            PlataformaService.eliminar_registro_base(p_id)

            # 🚀 El toque maestro: Si todo salió bien, guardamos todo de golpe en MariaDB
            db.session.commit()
            return True

        except Exception as e:
            # 🛡️ Si algo falla en cualquier punto, revertimos todo y no se borra nada
            db.session.rollback()
            raise e
    
    @staticmethod
    def panel_usuarios(filtros):

        # Lista de plataformas
        plataformas = PlataformaService.obtener_todas()
        
        # Extraer valores
        query_text = filtros.get('query', '').strip()
        plat_id = filtros.get('plataforma_id', '').strip()

        # Filtro
        if query_text or plat_id:
            usuarios = UsuarioService.filtrar_usuarios(
                busqueda=query_text, 
                plataforma_id=plat_id
            )
        else:
            usuarios = UsuarioService.obtener_todos()

        return {
            'listaPlataformas' : plataformas,
            'listaUsuarios' : usuarios,
            'filtros_usados' : filtros
        }
    
    @staticmethod
    def guardar_usuario(usuario_id, datos):
        ahora = datetime.now()
        mes_actual = ahora.month
        anio_actual = ahora.year
        # 1. FLUJO DE ACTUALIZACIÓN (EDITAR)
        if usuario_id and str(usuario_id).strip():
            u = UsuarioService.editar_usuario(int(usuario_id), datos)
            
            if u:
                plataformas_nuevas = set(datos.get('plataformas', []))
                plataformas_actuales = set([p.id for p in u.plataformas])

                eliminar = plataformas_actuales - plataformas_nuevas
                agregar = plataformas_nuevas - plataformas_actuales
                
                # Eliminar cobros pendientes de las plataformas desvinculadas
                for p_id in eliminar:
                    relacion = PlataformaUsuarioService.obtener_relacion(u.id, p_id)
                    CobroService.desvincular_pagos_pendientes(relacion.id)

                # Actualizar
                PlataformaUsuarioService.desvincular_plataformas(u.id, eliminar)
                PlataformaUsuarioService.vincular_plataformas(u.id, agregar)

                # Crear cobros de los nuevos vinculos
                for p_id in agregar:
                    try:
                        AdminService.crear_pago(u.id, int(p_id), mes_actual, anio_actual)
                    except ValueError as e:
                        flash(f"Aviso en cobros: {str(e)}", "warning")

            flash('Usuario actualizado correctamente.', 'success')        
            return u
            
            
        # 2. FLUJO DE CREACIÓN (NUEVO)
        else:
            u = UsuarioService.nuevo_usuario(datos)
            if u:
                mensaje = f"¡{u.nombres} {u.apeP} creado correctamente!"
                flash(mensaje, "success")



                # Extraer las plataformas directamente de los datos del formulario/request
                # Usamos .get() con una lista vacía [] por si el usuario se creó sin plataformas
                plataformas_ids = datos.get('plataformas', [])

                for p_id in plataformas_ids:
                    try:
                        # Orquestamos la creación del cobro estándar para cada plataforma asociada
                        AdminService.crear_pago(u.id, int(p_id), mes_actual, anio_actual)
                    except ValueError as e:
                        # Si un cobro falla (ej. ya existía), lo atrapamos para que no detenga el flujo de las demás
                        flash(f"Aviso en cobros: {str(e)}", "warning")
                
                return u
            else:
                flash("Error al crear el usuario.", "danger")
                return None

    @staticmethod
    def crear_pago(u_id, p_id, mes, anio):
        fechaCobro = date(int(anio), int(mes), 1)
        relacion = PlataformaUsuarioService.obtener_relacion(u_id, p_id)

        # Validar relacion usuario-plataforma
        if not relacion:
            raise ValueError("El usuario no está asignado a esta plataforma.")

        #  Verificar si ya hay un cobro para ese mes
        if CobroService.existe_cobro(relacion.id, fechaCobro):
            raise ValueError("Ya existe un cobro de este usuario para este periodo.")
        
        # 3. Obtener la plataforma de forma segura
        plataforma = db.session.get(Plataforma, p_id)
        if not plataforma:
            raise ValueError("La plataforma especificada no existe.")
        
        cuota_base = Decimal(str(plataforma.cuota))

        # Crear el cobro
        datos = {
            "usuario_plataforma_id": relacion.id,
            "mes_anio": fechaCobro,
            "monto_deuda": cuota_base,
            "estado": "pendiente"
        }

        return CobroService.crear_pago(datos)