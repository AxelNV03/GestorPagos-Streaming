# app/services/cobro_service.py
# ===================================================================================================
from app.core.models.cobro import Cobro
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.core.models.usuario import Usuario
from app.core.models.cobro import Cobro 
from app.core.models.comprobante import Comprobante

from datetime import date
from dateutil.relativedelta import relativedelta
from app import db
from sqlalchemy import func, or_
from sqlalchemy import or_, desc, extract, case
from sqlalchemy.orm import joinedload
from flask import flash
# ===================================================================================================
class CobroService:
    @staticmethod
    def metricas_globales_periodo(mes, anio):
        fecha_filtro = date(int(anio), int(mes), 1)

        # Resumen general
        resultado = db.session.query(
            func.sum(func.if_(Cobro.estado == 'pagado', Cobro.monto_deuda, 0.0)).label('recaudado'),
            func.sum(func.if_(Cobro.estado != 'pagado', Cobro.monto_deuda, 0.0)).label('restante'),
            func.count(Cobro.id).label('total_cobros'),
            func.count(func.if_(Cobro.estado == 'pagado', Cobro.id, None)).label('pagados')
        ).filter(Cobro.mes_anio == fecha_filtro).first()

        recaudado = float(resultado.recaudado or 0.0)
        restante = float(resultado.restante or 0.0)

        return {
            'recaudado':      recaudado,
            'restante':       restante,
            'total_esperado': recaudado + restante,
            'pagos':          int(resultado.pagados or 0),
            'users':          int(resultado.total_cobros or 0),
            'tiene_datos':    (resultado.total_cobros or 0) > 0
        }
# ===================================================================================================
    @staticmethod
    def metricas_plataformas_periodo(mes, anio):
        fecha_filtro = date(int(anio), int(mes), 1)
        resultados = db.session.query(
            PlataformaUsuario.plataforma_id,
            func.sum(func.if_(Cobro.estado == 'pagado', Cobro.monto_deuda, 0.0)).label('recaudado'),
            func.sum(func.if_(Cobro.estado != 'pagado', Cobro.monto_deuda, 0.0)).label('restante'),
            func.count(func.if_(Cobro.estado == 'pagado', Cobro.id, None)).label('pagados'),
            func.count(PlataformaUsuario.id).label('total_vinculos')
        ).join(
            Cobro, Cobro.usuario_plataforma_id == PlataformaUsuario.id
        ).filter(
            Cobro.mes_anio == fecha_filtro
        ).group_by(
            PlataformaUsuario.plataforma_id
        ).all()

        mapa_metricas = {}
        for r in resultados:
            mapa_metricas[r.plataforma_id] = {
                "finanzas": {
                    "recaudado": float(r.recaudado or 0.0),
                    "restante": float(r.restante or 0.0),
                    "total_esperado": float((r.recaudado or 0.0) + (r.restante or 0.0))
                },
                "conteos": {
                    "pagados": int(r.pagados or 0),
                    "no_pagados": int((r.total_vinculos or 0) - (r.pagados or 0)),
                    "total_usuarios": int(r.total_vinculos or 0)
                }
            }
        return mapa_metricas
# ===================================================================================================
    @staticmethod
    def obtener_cobros_de_usuarios(id_usuarios, mes, anio, estado=None):
        # Creamos la fecha exacta para comparar contra tu columna 'mes_anio' (Date)
        fecha_filtro = date(int(anio), int(mes), 1)
        
        query = db.session.query(Cobro).join(Cobro.suscripcion)\
            .options(
                joinedload(Cobro.comprobante_ref),
                joinedload(Cobro.suscripcion).joinedload(PlataformaUsuario.perfil_usuario),
                joinedload(Cobro.suscripcion).joinedload(PlataformaUsuario.plataforma)
            )
        
        # Filtros rápidos indexados
        query = query.filter(PlataformaUsuario.usuario_id.in_(id_usuarios))
        query = query.filter(Cobro.mes_anio == fecha_filtro)
        if estado:
            query = query.filter(Cobro.estado == estado)       
        # Mandamos los cobros pendientes (sin comprobante subido) al inicio de la tabla
        comprobante_null_primero = case((Cobro.comprobante_id.is_(None), 0), else_=1)
        query = query.outerjoin(Cobro.comprobante_ref)
        
        return query.order_by(
            comprobante_null_primero,
            desc(Comprobante.created_at),
            desc(Cobro.id)
        ).all()
# ===================================================================================================
    @staticmethod
    def obtener_cobros_usuario(usuario_id, estado=None):
        """Obtiene todos los cobros de un usuario, opcionalmente filtrados por estado"""
        query = db.session.query(Cobro).join(Cobro.suscripcion)\
            .options(
                joinedload(Cobro.comprobante_ref),
                joinedload(Cobro.suscripcion).joinedload(PlataformaUsuario.perfil_usuario),
                joinedload(Cobro.suscripcion).joinedload(PlataformaUsuario.plataforma)
            )\
            .filter(PlataformaUsuario.usuario_id == usuario_id)
        
        if estado:
            query = query.filter(Cobro.estado == estado)
        
        return query.order_by(Cobro.mes_anio.asc()).all()
# ===================================================================================================
    @staticmethod
    def clasificar_pendientes_por_tipo(usuario_id):
        """
        Devuelve los cobros pendientes de un usuario separados en:
        - mensualidades: agrupados por plataforma
        - extras: cobros únicos no recurrentes
        """

        # Solo cobros del mes actual
        cobros_pendientes = CobroService.obtener_cobros_usuario(usuario_id, estado='pendiente')
        inicio_mes = date.today().replace(day=1)
        cobros_pendientes = [c for c in cobros_pendientes if c.mes_anio == inicio_mes]
        
        mensualidades_por_plataforma = {}
        extras = []
        
        for c in cobros_pendientes:
            vinculo = c.suscripcion
            
            if c.motivo and c.motivo.startswith('Mensualidad'):
                if vinculo.id not in mensualidades_por_plataforma:
                    # Último pago de mensualidad de esta plataforma
                    todos_pagados = CobroService.obtener_cobros_usuario(usuario_id, estado='pagado')
                    ultimo = [x for x in todos_pagados 
                            if x.usuario_plataforma_id == vinculo.id 
                            and x.motivo and x.motivo.startswith('Mensualidad')]
                    ultimo = ultimo[-1] if ultimo else None
                    
                    mensualidades_por_plataforma[vinculo.id] = {
                        'plataforma': vinculo.plataforma.nombre,
                        'plataforma_usuario_id': vinculo.id,
                        'ultimo_pago': ultimo.mes_anio.strftime('%d/%m/%Y') if ultimo else None,
                        'pendientes': 0,
                        'cobros_ids': [],
                        'costo_mensual': float(c.monto_deuda)  # ← NUEVO
                    }
                
                mensualidades_por_plataforma[vinculo.id]['pendientes'] += 1
                mensualidades_por_plataforma[vinculo.id]['cobros_ids'].append(c.id)
            else:
                extras.append({
                    'cobro_id': c.id,
                    'plataforma': vinculo.plataforma.nombre,
                    'concepto': c.motivo or 'Sin concepto',
                    'monto': float(c.monto_deuda)
                })
        
        return {
            'mensualidades': list(mensualidades_por_plataforma.values()),
            'extras': extras
        }
# ===================================================================================================
    # up_id = usuario_plataforma_id
    @staticmethod
    def existe_cobro(up_id, fecha):
        return db.session.query(
            db.session.query(Cobro).filter_by(
                usuario_plataforma_id=up_id,
                mes_anio=fecha
            ).exists()
        ).scalar()
# ===================================================================================================
    @staticmethod
    def nuevo_cobro(datos):
        nuevo_cobro = Cobro(
            usuario_plataforma_id=datos["usuario_plataforma_id"],
            comprobante_id=None,
            mes_anio=datos["mes_anio"],
            monto_deuda=datos["monto_deuda"],
            estado=datos["estado"],
            motivo=datos["motivo"]
        )
        db.session.add(nuevo_cobro)

        return nuevo_cobro
# ===================================================================================================
    @staticmethod
    def eliminar_pagos_pendientes_de_usuario(up_id):
        db.session.query(Cobro).filter_by(
            usuario_plataforma_id=up_id,
            estado='pendiente'
        ).delete(synchronize_session=False)
# ===================================================================================================
    @staticmethod
    def eliminar_cobros_de_plataforma(vinculos_ids):
        """Borra los cobros vinculados a la lista de users recibida"""
        return db.session.query(Cobro).filter(
            Cobro.usuario_plataforma_id.in_(vinculos_ids)
        ).delete(synchronize_session=False)
# ===================================================================================================
    @staticmethod
    def actualizar_monto_cobros_pendientes(lista_up_ids, nuevo_monto):
        """Actualiza todos los cobros pendientes de una lista de plataformas"""
        if lista_up_ids and nuevo_monto is not None:
            db.session.query(Cobro).filter(
                Cobro.usuario_plataforma_id.in_(lista_up_ids),
                Cobro.estado == 'pendiente'
            ).update(
                {Cobro.monto_deuda: float(nuevo_monto)}, 
                synchronize_session=False
            )
# ===================================================================================================
    @staticmethod
    def eliminar_pagos_pendientes_de_usuario_en_plataformas(usuario_id, id_plataformas):
        if not id_plataformas:
            return
            
        db.session.query(Cobro).filter(
            Cobro.usuario_plataforma_id.in_(
                db.session.query(PlataformaUsuario.id).filter(
                    PlataformaUsuario.usuario_id == usuario_id,
                    PlataformaUsuario.plataforma_id.in_(id_plataformas)
                )
            ),
            Cobro.estado == 'pendiente'
        ).delete(synchronize_session=False)
# ===================================================================================================
    @staticmethod
    def generar_pagos_futuros(plataforma_usuario_id, cantidad_meses):
        """Genera cobros de mensualidad pendientes para los próximos N meses"""
        
        MESES_ES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        ultimo = Cobro.query.filter(
            Cobro.usuario_plataforma_id == plataforma_usuario_id,
            Cobro.motivo.like('Mensualidad%')
        ).order_by(Cobro.mes_anio.desc()).first()
        
        if not ultimo:
            return
        
        vinculo = ultimo.suscripcion
        
        for i in range(1, cantidad_meses + 1):
            siguiente_mes = ultimo.mes_anio + relativedelta(months=i)
            label = f"{MESES_ES[siguiente_mes.month - 1]} {siguiente_mes.year}"
            
            if CobroService.existe_cobro(plataforma_usuario_id, siguiente_mes):
                continue
            
            cobro = Cobro(
                usuario_plataforma_id=plataforma_usuario_id,
                mes_anio=siguiente_mes,
                monto_deuda=ultimo.monto_deuda,
                estado='pendiente',
                motivo=f"Mensualidad - {vinculo.plataforma.nombre} ({label})"
            )
            db.session.add(cobro)
# ===================================================================================================
    @staticmethod
    def cubrir_mensualidades(plataforma_usuario_id, cantidad_meses, comprobante_id):
        """Asigna los N cobros pendientes más antiguos al comprobante y los marca como pagado"""
        cobros = Cobro.query.filter(
            Cobro.usuario_plataforma_id == plataforma_usuario_id,
            Cobro.estado == 'pendiente',
            Cobro.motivo.like('Mensualidad%')
        ).order_by(Cobro.mes_anio.asc()).limit(cantidad_meses).all()
        
        for cobro in cobros:
            cobro.comprobante_id = comprobante_id
            cobro.estado = 'pagado'
# ===================================================================================================
    @staticmethod
    def asignar_extra(cobro_id, comprobante_id):
        cobro = db.session.get(Cobro, cobro_id)
        if cobro and cobro.estado == 'pendiente':
            cobro.comprobante_id = comprobante_id
            cobro.estado = 'pagado'