# app/services/admin_service.py
# ===================================================================================================
from app.services.usuario_service import UsuarioService
from app.services.plataforma_service import PlataformaService
from app.services.plataforma_usuario_service import PlataformaUsuarioService
from app.services.cobro_service import CobroService
from app.services.periodo_service import PeriodoService
from app.core.models.plataforma import Plataforma
from app.core.models.usuario import Usuario
from app.core.models.cobro import Cobro
from app.core.models.plataforma_usuario import PlataformaUsuario

from itertools import groupby
from operator import attrgetter
from app import db
from flask import flash
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
# ===================================================================================================
class AdminService:
    @staticmethod
    def _inyectar_metricas_plataformas(plataformas, mapa_metricas):
        for p in plataformas:
            metricas_individuales = mapa_metricas.get(p.id, {
                "finanzas": {"recaudado": 0.0, "restante": 0.0, "total_esperado": 0.0},
                "conteos": {"pagados": 0, "no_pagados": 0, "total_usuarios": 0}
            })            
            p.finanzas = metricas_individuales["finanzas"]
            p.conteos = metricas_individuales["conteos"]
        
        return plataformas
# ===================================================================================================
    @staticmethod
    def dashboard_data():
        info_p = PeriodoService.obtener_periodo_actual()
        mes, anio, label = info_p["mes"], info_p["anio"], info_p["label"]

        finanzas = CobroService.metricas_globales_periodo(mes, anio)
        mapa_metricas = CobroService.metricas_plataformas_periodo(mes, anio)
        plataformasB = PlataformaService.obtener_todas()
        plataformas = AdminService._inyectar_metricas_plataformas(plataformasB, mapa_metricas)
        plataformas_deudoras = [p for p in plataformas if p.conteos['no_pagados'] > 0]

        return {
            "periodo": {
                "label": label,
                "total_recaudado": finanzas['recaudado'],
                "total_restante": finanzas['restante']
            },
            "plataformas": plataformas,  
            "plataformas_pendientes": plataformas_deudoras
        }
# ===================================================================================================



# ===================================================================================================
# SECCION DE PLATAFORMAS
# ===================================================================================================
    @staticmethod
    def panel_plataformas():
        info_p = PeriodoService.obtener_periodo_actual()
        mes, anio, label = info_p["mes"], info_p["anio"], info_p["label"]

        metricas_g = CobroService.metricas_globales_periodo(mes, anio)
        metricas_p = CobroService.metricas_plataformas_periodo(mes, anio)
        plataformas = PlataformaService.obtener_todas()        
        plataformas_info = AdminService._inyectar_metricas_plataformas(plataformas, metricas_p)

        return {
            'periodo' : label, 
            'plataformas' : plataformas_info,
            'metricas': metricas_g 
        }
# ===================================================================================================
    @staticmethod
    def guardar_plataforma(plataforma_id, datos, archivo_logo):     
        try:
            if plataforma_id and plataforma_id.strip():
                
                plataforma = db.session.get(Plataforma, plataforma_id)                            

                debe_actualizar_cobros = (float(plataforma.cuota) != float(datos['cuota']))
                
                p_actualizada = PlataformaService.editar_plataforma(plataforma, datos, archivo_logo)
                
                if debe_actualizar_cobros:
                    relaciones_ids = PlataformaUsuarioService.obtener_vinculos_de_plataforma(p_actualizada.id)
                    CobroService.actualizar_monto_cobros_pendientes(relaciones_ids, p_actualizada.cuota)
            else:
                PlataformaService.nueva_plataforma(datos, archivo_logo)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
# ===================================================================================================
    @staticmethod
    def borrar_plataforma(plataforma_id):
        try:
            p = db.session.get(Plataforma, plataforma_id)
            if not p:
                raise Exception("La plataforma que intentas eliminar no existe.")
            
            relaciones_ids = PlataformaUsuarioService.obtener_vinculos_de_plataforma(p.id)
            if relaciones_ids:
                CobroService.eliminar_cobros_de_plataforma(relaciones_ids)
            
            PlataformaUsuarioService.desvincular_usuarios_de_plataforma(p.id)
            PlataformaService.eliminar_plataforma_db(p)
            db.session.flush()

            PlataformaService.eliminar_archivo_logo(p)
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            raise e
# ===================================================================================================



# ===================================================================================================
# SECCION DE USUARIOS
# ===================================================================================================
    @staticmethod
    def panel_usuarios(filtros):
        plataformas = PlataformaService.obtener_todas()
        usuarios = UsuarioService.filtrar_usuarios(
            busqueda=filtros.get('query'), 
            plataforma_id=filtros.get('plataforma_id')
        )
        return {
            'listaPlataformas': plataformas,
            'listaUsuarios': usuarios,
            'filtros_usados': filtros
        }
# ===================================================================================================
    @staticmethod
    def guardar_usuario(usuario_id, datos):
        info_p = PeriodoService.obtener_periodo_actual()
        mes_actual, anio_actual, label = info_p["mes"], info_p["anio"], info_p["label"]

        try:
            # ================================================================
            # 1. EDITAR
            # ================================================================
            if usuario_id and str(usuario_id).strip():
                u = UsuarioService.editar_usuario(int(usuario_id), datos)
                if not u:
                    raise Exception("El usuario que intentas editar no existe.")

                plataformas_nuevas = set(datos.get('plataformas', []))
                plataformas_actuales = set([p.id for p in u.plataformas])

                eliminar = plataformas_actuales - plataformas_nuevas
                agregar = plataformas_nuevas - plataformas_actuales

                if eliminar:
                    CobroService.eliminar_pagos_pendientes_de_usuario_en_plataformas(u.id, eliminar)
                    PlataformaUsuarioService.desvincular_plataformas_de_usuario(u.id, eliminar)

                if agregar:
                    PlataformaUsuarioService.vincular_plataformas_a_usuario(u.id, agregar)                    
                    db.session.flush()
                    AdminService.generar_cobros_en_plataformas(u.id, agregar, mes_actual, anio_actual, label)
                                
            # 2. FLUJO DE CREACIÓN (NUEVO)
            else:
                u = UsuarioService.nuevo_usuario(datos)
                if not u:
                    raise Exception("No se pudo registrar el usuario en el sistema.")

                plataformas_ids = datos.get('plataformas', [])
                if plataformas_ids:
                    PlataformaUsuarioService.vincular_plataformas_a_usuario(u.id, plataformas_ids)         
                    db.session.flush()       
                    AdminService.generar_cobros_en_plataformas(u.id, plataformas_ids, mes_actual, anio_actual, label)
            
            db.session.commit()
            return u
        except Exception as e:
            # 🛡️ Al más mínimo error en CUALQUIERA de los dos flujos, limpiamos la sesión por completo.
            # No se guardará nada roto, incompleto o a medias. ¡Todo o Nada!
            db.session.rollback()
            raise e
# ===================================================================================================
    @staticmethod
    def generar_cobros_en_plataformas(usuario_id, id_plataformas, mes, anio, label):
        if not id_plataformas:
            return
        
        fecha_cobro = date(int(anio), int(mes), 1)


        # 1. Traemos de un solo golpe los contratos que se acaban de crear/activar
        relaciones = db.session.query(PlataformaUsuario).filter(
            PlataformaUsuario.usuario_id == usuario_id,
            PlataformaUsuario.plataforma_id.in_(id_plataformas),
            PlataformaUsuario.activo == 1
        ).all()
        mapa_relaciones = {r.plataforma_id: r for r in relaciones}

        # 2. Traemos de un solo golpe los precios de esas plataformas
        plataformas = db.session.query(Plataforma).filter(
            Plataforma.id.in_(id_plataformas)
        ).all()

        nuevos_cobros = []

        for plat in plataformas:
            relacion = mapa_relaciones.get(plat.id)
            if not relacion:
                raise ValueError(f"Error crítico: No se encontró el contrato activo para la plataforma {plat.nombre}.")
                        
            if CobroService.existe_cobro(relacion.id, fecha_cobro):
                continue 

            # Construimos el objeto de cobro con su motivo súper descriptivo
            cobro_objeto = Cobro(
                usuario_plataforma_id=relacion.id,
                mes_anio=fecha_cobro,
                monto_deuda=Decimal(str(plat.cuota)),
                estado="pendiente",
                motivo=f"Mensualidad - {plat.nombre} ({label})"
            )
            nuevos_cobros.append(cobro_objeto)

        if nuevos_cobros:
            db.session.add_all(nuevos_cobros)
# ===================================================================================================


# ===================================================================================================
# SECCION DE COBROS
# ===================================================================================================
    @staticmethod
    def panel_cobros(filtros):                
        plataformas = PlataformaService.obtener_todas()
        usuarios = UsuarioService.obtener_todos()
        usuariosF = UsuarioService.filtrar_usuarios(
            busqueda=filtros.get('query'), 
            plataforma_id=filtros.get('plataforma_id')
        )

        if not usuariosF:
            return {
                'listaPlataformas': plataformas,
                'mes_actual': filtros["mes"],
                'anio_actual': filtros["anio"],
                'filtros_usados': filtros,
                'cobros': []  # Lista vacía, no diccionario
            }
        
        lista_ids = [u.id for u in usuariosF]
        cobros = CobroService.obtener_cobros_de_usuarios(
            lista_ids, filtros["mes"], filtros["anio"]
        )
        
        cobros_ordenados = sorted(cobros, key=lambda c: c.suscripcion.perfil_usuario.id)        
        cobros_agrupados = []
        for key, group in groupby(cobros_ordenados, key=lambda c: c.suscripcion.perfil_usuario.id):
            grupo_cobros = list(group)
            cobros_agrupados.append({
                'usuario': grupo_cobros[0].suscripcion.perfil_usuario,
                'cobros': grupo_cobros,
                'total_grupo': sum(c.monto_deuda for c in grupo_cobros),
                'es_multiple': len(grupo_cobros) > 1
            })
        
        return {
            'listaPlataformas': plataformas,
            'mes_actual': filtros["mes"],
            'anio_actual': filtros["anio"],
            'filtros_usados': filtros,
            'cobros': cobros_agrupados,  
            'usuarios': usuarios
        }
# ===================================================================================================
    @staticmethod
    def cobro_extra(datos):
        # Datos del periodo
        info_p = PeriodoService.obtener_periodo_actual()
        mes_actual, anio_actual, label = info_p["mes"], info_p["anio"], info_p["label"]
        fecha_cobro = date(int(anio_actual), int(mes_actual), 1)
        
        # Desempaquetado de datos
        alcance = datos.get('alcance')
        monto = datos.get('monto')
        concepto = datos.get('concepto')
        usuario_id = datos.get('usuario_id')
        plataforma_id = datos.get('plataforma_id')
        
        try:
            # 1. Cobro general de plataforma
            if alcance == 'plataforma':
                usuarios_plataforma = PlataformaUsuarioService.obtener_vinculos_de_plataforma(plataforma_id)
                if not usuarios_plataforma:
                    raise Exception("La plataforma no cuenta con usuarios asociados")
                
                for vinculo_id in usuarios_plataforma:
                    nuevo_cobro = Cobro(
                        usuario_plataforma_id=vinculo_id,
                        mes_anio=fecha_cobro,
                        monto_deuda=Decimal(str(monto)),
                        estado='pendiente',
                        motivo=concepto
                    )
                    db.session.add(nuevo_cobro)
                db.session.commit()
            else:
                # 2. Cobro a un solo user
                # Buscamos el vínculo activo entre el usuario y la plataforma elegida en el selector interactivo
                vinculo = PlataformaUsuario.query.filter_by(
                    usuario_id=int(usuario_id),
                    plataforma_id=int(plataforma_id),
                    activo=True
                ).first()

                if not vinculo:
                    raise Exception("Se necesita indicar la plataforma")

                nuevo_cobro = Cobro(
                    usuario_plataforma_id=vinculo.id,
                    mes_anio=fecha_cobro,
                    monto_deuda=Decimal(str(monto)),
                    estado='pendiente',
                    motivo=concepto
                )
                db.session.add(nuevo_cobro)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
# ===================================================================================================
    @staticmethod
    def eliminar_cobro(cobro_id):
        try: 
            cobro = db.session.get(Cobro, cobro_id)

            if not cobro:
                raise ValueError('Cobro no encontrado')
            if cobro.estado != 'pendiente':
                raise ValueError('Solo se pueden eliminar cobros pendientes')

            db.session.delete(cobro)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
# ===================================================================================================
    @staticmethod
    def editar_cobro(cobro_id, datos):
        try:
            cobro = db.session.get(Cobro, cobro_id)
            if not cobro:
                raise ValueError('Cobro no encontrado')
            if cobro.estado != 'pendiente':
                raise ValueError('Solo se pueden editar cobros pendientes')
            
            motivo = datos.get('motivo', '').strip()
            monto = datos.get('monto')
            
            # Validaciones
            if not motivo:
                raise ValueError('El motivo no puede estar vacío')
            
            try:
                monto_decimal = Decimal(str(monto))
            except:
                raise ValueError('El monto no es válido')
            
            if monto_decimal <= 0:
                raise ValueError('El monto debe ser mayor a $0')
            
            if monto_decimal > 999999.99:
                raise ValueError('El monto excede el límite permitido')
            
            # Verificar si realmente hubo cambios
            if cobro.motivo == motivo and cobro.monto_deuda == monto_decimal:
                return False  # No hubo cambios
            
            cobro.motivo = motivo
            cobro.monto_deuda = monto_decimal
            db.session.commit()
            return True  # Sí se actualizó
            
        except Exception as e:
            db.session.rollback()
            raise e