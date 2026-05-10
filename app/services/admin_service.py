# app/services/admin_service.py
# ===================================================================================================
from app.services.usuario_service import UsuarioService
from app.services.plataforma_service import PlataformaService
from app.services.cobro_service import CobroService
from app.services.periodo_service import PeriodoService

from app import db
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
        plataformas_deudoras = PlataformaService.pendientes_periodo(info_p['mes'], info_p['anio'])

        # 4. Mapeamos a una lista de diccionarios (limpios para el HTML)
        lista_pendientes = [
            {
                "id": p.id,
                "nombre": p.nombre,
                "precio": p.precio_total
            } for p in plataformas_deudoras
        ]

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
            "plataformas_pendientes": lista_pendientes  # <--- Enviamos la lista aquí
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
        from app.core.models.plataforma import Plataforma
        if plataforma_id and plataforma_id.strip():
            # Edición
            p = Plataforma.query.get_or_404(plataforma_id)            
            precio_anterior = float(p.precio_total)
            precio_nuevo = float(datos['precio_total'])
            
            # Actualizamos los datos del modelo
            p.nombre = datos['nombre']
            p.precio_total = precio_nuevo
            p.dia_cobro = datos['dia_cobro']
            p.cuota = datos['cuota'] 
            p.correo_admin = datos['correo_admin']

            p_actualizada = PlataformaService.editar_plataforma(plataforma_id, datos, archivo_logo)


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