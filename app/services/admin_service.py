# app/services/admin_service.py
# ===================================================================================================
from app.services.usuario_service import UsuarioService
from app.services.plataforma_service import PlataformaService
from app.services.plataforma_usuario_service import PlataformaUsuarioService
from app.services.cobro_service import CobroService
from app.services.periodo_service import PeriodoService
from app.services.comprobante_service import ComprobanteService
from app.services.email_service import EmailService

from app.core.models.plataforma import Plataforma
from app.core.models.cobro import Cobro
from app.core.models.comprobante import Comprobante
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.core.models.usuario import Usuario


from itertools import groupby
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from operator import attrgetter
from app import db
import os
from flask import flash, current_app
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
            "plataformas_pendientes": plataformas_deudoras,
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
    @staticmethod
    def panel_plataforma(plataforma_id, params):
        info_p = PeriodoService.obtener_periodo_actual()
        mes = int(params.get('mes') or info_p['mes'])
        anio = int(params.get('anio') or info_p['anio'])
        
        plataforma = db.session.get(Plataforma, plataforma_id)
        if not plataforma:
            raise ValueError('Plataforma no encontrada')
        
        vinculos = PlataformaUsuario.query.filter_by(
            plataforma_id=plataforma_id, activo=True
        ).options(joinedload(PlataformaUsuario.perfil_usuario)).all()
        
        usuarios_data = []
        total_pagado = 0
        total_pendiente = 0
        
        for v in vinculos:
            cobros = Cobro.query.filter(
                Cobro.usuario_plataforma_id == v.id,
                func.extract('month', Cobro.mes_anio) == int(mes),
                func.extract('year', Cobro.mes_anio) == int(anio)
            ).all()
            
            pagado = sum(c.monto_deuda for c in cobros if c.estado == 'pagado')
            pendiente = sum(c.monto_deuda for c in cobros if c.estado == 'pendiente')
            
            total_pagado += pagado
            total_pendiente += pendiente
            
            usuarios_data.append({
                'usuario': v.perfil_usuario,
                'pagado': pagado,
                'pendiente': pendiente
            })
        
        MESES_ES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        label = f"{MESES_ES[int(mes)-1]} {anio}"
        
        return {
            'plataforma': plataforma,
            'usuarios_data': usuarios_data,
            'total_pagado': total_pagado,
            'total_pendiente': total_pendiente,
            'total_usuarios': len(vinculos),
            'label': label,
            'mes_actual': mes,
            'anio_actual': anio
        }
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
                    PlataformaUsuarioService.vincular_plataformas_a_usuario(
                        u.id, agregar, datos.get('correos_plataforma', {})
                    )               
                    db.session.flush()
                    AdminService.generar_cobros_en_plataformas(u.id, agregar, mes_actual, anio_actual, label)

                # ✅ Actualizar correos de plataformas existentes
                correos_dict = datos.get('correos_plataforma', {})
                for p_id in plataformas_nuevas:
                    vinculo = PlataformaUsuario.query.filter_by(
                        usuario_id=u.id, plataforma_id=p_id, activo=1
                    ).first()
                    if vinculo and p_id in correos_dict:
                        vinculo.correo_plataforma = correos_dict.get(p_id)
                                
            else:
                u = UsuarioService.nuevo_usuario(datos)
                if not u:
                    raise Exception("No se pudo registrar el usuario en el sistema.")

                plataformas_ids = datos.get('plataformas', [])
                if plataformas_ids:
                    PlataformaUsuarioService.vincular_plataformas_a_usuario(
                        u.id, plataformas_ids, datos.get('correos_plataforma', {})
                    )
                    db.session.flush()       
                    AdminService.generar_cobros_en_plataformas(u.id, plataformas_ids, mes_actual, anio_actual, label)
            
            db.session.commit()

            # Dar la bienvenida
            if not usuario_id or not str(usuario_id).strip():
                # Es usuario nuevo
                usuario = u  # u es el usuario creado
                if usuario.correo:
                    EmailService.bienvenida(usuario)
            return u
        except Exception as e:
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
    @staticmethod
    def panel_usuario(usuario_id, params):
        info_p = PeriodoService.obtener_periodo_actual()
        mes = int(params.get('mes') or info_p['mes'])
        anio = int(params.get('anio') or info_p['anio'])
        
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError('Usuario no encontrado')
        
        # Cobros del mes
        cobros = Cobro.query.join(Cobro.suscripcion).filter(
            PlataformaUsuario.usuario_id == usuario_id,
            func.extract('month', Cobro.mes_anio) == int(mes),
            func.extract('year', Cobro.mes_anio) == int(anio)
        ).options(
            joinedload(Cobro.comprobante_ref),
            joinedload(Cobro.suscripcion).joinedload(PlataformaUsuario.plataforma)
        ).order_by(Cobro.mes_anio.asc()).all()
        
        total_deuda = sum(c.monto_deuda for c in cobros if c.estado == 'pendiente')
        total_pagado = sum(c.monto_deuda for c in cobros if c.estado == 'pagado')
        plataformas_activas = len([s for s in usuario.suscripciones if s.activo])
        
        comprobantes = Comprobante.query.filter_by(usuario_id=usuario_id)\
            .order_by(Comprobante.created_at.desc()).limit(5).all()
        
        label = f"{mes}/{anio}"
        
        return {
            'usuario': usuario,
            'cobros': cobros,
            'total_deuda': total_deuda,
            'total_pagado': total_pagado,
            'plataformas_activas': plataformas_activas,
            'comprobantes': comprobantes,
            'label': label,
            'mes_actual': mes,
            'anio_actual': anio
        }
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
            lista_ids, filtros["mes"], filtros["anio"], filtros["estado"]
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

        comprobantes_mes = ComprobanteService.obtener_comprobantes_del_mes(
            filtros["mes"], filtros["anio"]
        )
        
        return {
            'listaPlataformas': plataformas,
            'mes_actual': filtros["mes"],
            'anio_actual': filtros["anio"],
            'filtros_usados': filtros,
            'cobros': cobros_agrupados,  
            'usuarios': usuarios,
            'comprobantes_mes': comprobantes_mes
        }
# ===================================================================================================
    @staticmethod
    def cobro_extra(datos):
        info_p = PeriodoService.obtener_periodo_actual()
        mes_actual, anio_actual, label = info_p["mes"], info_p["anio"], info_p["label"]
        fecha_cobro = date(int(anio_actual), int(mes_actual), 1)
        
        alcance = datos.get('alcance')
        monto = datos.get('monto')
        concepto = datos.get('concepto')
        usuario_id = datos.get('usuario_id')
        plataforma_id = datos.get('plataforma_id')
        
        try:
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
                
                # Notificar a todos los usuarios de la plataforma
                plataforma = db.session.get(Plataforma, plataforma_id)
                if plataforma:
                    for v in plataforma.usuarios_vinculados:
                        if v.activo and v.perfil_usuario.correo:
                            EmailService.nuevo_cargo_extra(v.perfil_usuario, concepto, monto, plataforma.nombre)
            else:
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
                
                # Notificar al usuario
                # Para notificar al usuario individual
                user = db.session.get(Usuario, int(usuario_id))
                if user and user.correo:
                    EmailService.nuevo_cargo_extra(user, concepto, monto, vinculo.plataforma.nombre)
                    
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
# ===================================================================================================



# ===================================================================================================
# SECCION DE COMPROBANTES
# ===================================================================================================
    @staticmethod
    def panel_comprobantes(filtros):
        info_p = PeriodoService.obtener_periodo_actual()
        plataformas = PlataformaService.obtener_todas()
        usuarios = UsuarioService.obtener_todos()
        
        comprobantes = ComprobanteService.obtener_comprobantes_del_mes(
            filtros["mes"], filtros["anio"], filtros.get("estado") or None
        )
        
        metricas = ComprobanteService.metricas_mes(filtros["mes"], filtros["anio"])
        
        # ✅ Bulk: traer todos los pendientes de todos los usuarios de los comprobantes
        usuarios_ids = list(set(comp.usuario_id for comp in comprobantes))
        pendientes_por_usuario = CobroService.clasificar_pendientes_bulk(
            usuarios_ids, 
            mes=filtros["mes"], 
            anio=filtros["anio"]
        ) if usuarios_ids else {}
                        
        datos_revision = {}
        for comp in comprobantes:
            datos_revision[comp.id] = pendientes_por_usuario.get(comp.usuario_id, {'mensualidades': [], 'extras': []})
        
        return {
            'listaPlataformas': plataformas,
            'usuarios': usuarios,
            'mes_actual': filtros["mes"],
            'anio_actual': filtros["anio"],
            'label': info_p["label"],
            'filtros_usados': filtros,
            'comprobantes': comprobantes,
            'metricas': metricas,
            'datos_revision': datos_revision
        }
# ===================================================================================================
    @staticmethod
    def subir_comprobante(usuario_id, archivo, nota):
        if not usuario_id:
            raise ValueError('Debe seleccionar un usuario')
        if not archivo or archivo.filename == '':
            raise ValueError('Debe seleccionar una imagen')
        
        try:
            ComprobanteService.guardar_comprobante(usuario_id, archivo, nota)
        except Exception as e:
            db.session.rollback()
            raise e
# ===================================================================================================
    @staticmethod
    def obtener_ruta_imagen(comprobante_id):
        comprobante = db.session.get(Comprobante, comprobante_id)
        if not comprobante:
            raise ValueError('Comprobante no encontrado')
        
        ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], comprobante.ruta_archivo)
        if not os.path.exists(ruta):
            raise ValueError('Archivo no encontrado')
        
        return ruta
# ===================================================================================================
    @staticmethod
    def aprobar_comprobante(comprobante_id, form_data):
        comprobante = db.session.get(Comprobante, comprobante_id)
        if not comprobante:
            raise ValueError('Comprobante no encontrado')
        if comprobante.estado != 'revision':
            raise ValueError('Solo se pueden aprobar comprobantes en revisión')
        
        comentario = form_data.get('comentario', '')
        
        try:
            for key, value in form_data.items():
                if key.startswith('meses_') and int(value) > 0:
                    plataforma_usuario_id = int(key.replace('meses_', ''))
                    CobroService.generar_pagos_futuros(plataforma_usuario_id, int(value))
                    CobroService.cubrir_mensualidades(plataforma_usuario_id, int(value), comprobante.id)
                elif key.startswith('extra_'):
                    cobro_id = int(key.replace('extra_', ''))
                    CobroService.asignar_extra(cobro_id, comprobante.id)
            
            ComprobanteService.cambiar_estado(comprobante, 'aprobado', comentario)
            db.session.refresh(comprobante)
            
            # Enviar correo
            AdminService._enviar_correo_aprobacion(comprobante, comentario)
                
        except Exception as e:
            db.session.rollback()
            raise e
    # ===================================================================================================
    @staticmethod
    def _enviar_correo_aprobacion(comprobante, comentario):
        """Prepara y envía el correo de comprobante aprobado"""
        usuario = comprobante.usuario
        if not usuario.correo:
            return
        
        cobros_cubiertos = [{
            'motivo': c.motivo or 'Mensualidad',
            'monto': float(c.monto_deuda),
        } for c in comprobante.cobros_asociados]

        total_cubierto = sum(c['monto'] for c in cobros_cubiertos)
        
        hoy = date.today()
        inicio_mes = hoy.replace(day=1)
        pendientes_q = Cobro.query.filter(
            Cobro.suscripcion.has(PlataformaUsuario.usuario_id == usuario.id),
            Cobro.estado == 'pendiente',
            Cobro.mes_anio == inicio_mes
        ).all()
        

        pendientes_lista = [{
            'motivo': p.motivo or 'Mensualidad',
            'monto': float(p.monto_deuda),
        } for p in pendientes_q]

        EmailService.comprobante_aprobado(
            usuario, cobros_cubiertos, total_cubierto, 
            pendientes_lista, comentario or None
        )
# ===================================================================================================
    @staticmethod
    def rechazar_comprobante(comprobante_id, comentario):
        comprobante = db.session.get(Comprobante, comprobante_id)
        if not comprobante:
            raise ValueError('Comprobante no encontrado')
        if comprobante.estado != 'revision':
            raise ValueError('Solo se pueden rechazar comprobantes en revisión')
        
        try:
            ComprobanteService.cambiar_estado(comprobante, 'rechazado', comentario)

            # Rechazado 
            # Email de rechazo
            usuario = comprobante.usuario
            if usuario.correo:
                EmailService.comprobante_rechazado(usuario, comentario or 'Sin motivo especificado')

        except Exception as e:
            db.session.rollback()
            raise e
# ===================================================================================================
# AdminService
    @staticmethod
    def enviar_anuncio(mensaje):
        if not mensaje.strip():
            raise ValueError('El mensaje no puede estar vacío')
        
        usuarios = UsuarioService.obtener_todos()
        enviados = 0
        for u in usuarios:
            if u.correo:
                EmailService.aviso_general(u, mensaje)
                enviados += 1
        return enviados