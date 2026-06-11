# app/services/cobro_service.py
# ===================================================================================================
from app.core.models.cobro import Cobro
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.services.plataforma_usuario_service import PlataformaUsuarioService
from app.core.models.cobro import Cobro 
from datetime import date
from app import db
from sqlalchemy import func, or_
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