from app.core.models.cobro import Cobro
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.services.plataforma_usuario_service import PlataformaUsuarioService

from datetime import date
from app import db
from sqlalchemy import func, or_
from flask import flash


class CobroService:
    @staticmethod
    def balance_global(mes, anio):
        from app.core.models.cobro import Cobro 
                
        fecha_filtro = date(anio, int(mes), 1)

        # 1. Suma de Pagados + Pendientes
        # Si no hay registros, .scalar() es None -> se convierte en 0.0
        total_esperado = db.session.query(func.sum(Cobro.monto_deuda)).filter(
            Cobro.mes_anio == fecha_filtro,
            or_(Cobro.estado == 'pagado', Cobro.estado == 'pendiente')
        ).scalar() or 0.0

        # 2. Suma de Pagados
        recaudado = db.session.query(func.sum(Cobro.monto_deuda)).filter(
            Cobro.mes_anio == fecha_filtro,
            Cobro.estado == 'pagado'
        ).scalar() or 0.0

        # 3. Cálculo matemático seguro entre flotantes
        restante = float(total_esperado) - float(recaudado)

        # Retornamos el diccionario con valores listos para el HTML
        return {
            'recaudado': float(recaudado),
            'restante': restante,
            'total_esperado': float(total_esperado),
            'tiene_datos': total_esperado > 0 # Útil para mostrar mensajes en el HTML
        }
    
    @staticmethod
    def conteo_pagos_periodo(mes, anio):
        """ Obtiene el total de cobros realizados vs los ya pagados del periodo actual. """
        fecha_filtro = date(int(anio), int(mes), 1)

        # 1. Total de cobros generados para este mes específico (activos del periodo)
        total_usuarios_periodo = db.session.query(func.count(Cobro.id)).filter(
            Cobro.mes_anio == fecha_filtro
        ).scalar() or 0

        # 2. Total de cobros que ya cambiaron su estado a 'pagado' en este mismo mes
        pagos_realizados = db.session.query(func.count(Cobro.id)).filter(
            Cobro.mes_anio == fecha_filtro,
            Cobro.estado.ilike('pagado') # 🛡️ Blindado contra mayúsculas/minúsculas
        ).scalar() or 0

        return {
            "pagos": pagos_realizados,
            "users": total_usuarios_periodo  # Refleja los usuarios reales con cobro este mes
        }
    
    @staticmethod
    def finanzas_plataforma(plataforma_id, mes, anio):
        fecha_filtro = date(anio, int(mes), 1)
        
        recaudado = db.session.query(func.sum(Cobro.monto_deuda))\
            .join(PlataformaUsuario, Cobro.usuario_plataforma_id == PlataformaUsuario.id)\
            .filter(
                PlataformaUsuario.plataforma_id == plataforma_id,
                Cobro.mes_anio == fecha_filtro,
                Cobro.estado == 'pagado'
            ).scalar() or 0.0

        restante = db.session.query(func.sum(Cobro.monto_deuda))\
            .join(PlataformaUsuario, Cobro.usuario_plataforma_id == PlataformaUsuario.id)\
            .filter(
                PlataformaUsuario.plataforma_id == plataforma_id,
                Cobro.mes_anio == fecha_filtro,
                Cobro.estado != 'pagado'  # Incluye pendiente y en_revision
        ).scalar() or 0.0

        return {
            "recaudado": float(recaudado),
            "restante": float(restante)
        }
    
    @staticmethod
    def conteo_pagos_plataforma(plataforma_id, mes, anio):
        fecha_filtro = date(anio, int(mes), 1)
        # 1. Total de usuarios asignados a esta plataforma
        total_usuarios = db.session.query(func.count(PlataformaUsuario.id))\
            .filter(PlataformaUsuario.plataforma_id == plataforma_id)\
            .scalar() or 0

        # 2. Total de pagos ya realizados en el mes para esta plataforma
        pagos_realizados = db.session.query(func.count(Cobro.id))\
            .join(PlataformaUsuario, Cobro.usuario_plataforma_id == PlataformaUsuario.id)\
            .filter(
                PlataformaUsuario.plataforma_id == plataforma_id,
                Cobro.mes_anio == fecha_filtro,
                Cobro.estado == 'pagado'
            ).scalar() or 0
        
        return {
            "pagados" : pagos_realizados,
            "no_pagados"  : total_usuarios - pagos_realizados
        }
    
    # up_id = usuario_plataforma_id
    @staticmethod
    def existe_cobro(up_id, fecha):
        return db.session.query(
            db.session.query(Cobro).filter_by(
                usuario_plataforma_id=up_id,
                mes_anio=fecha
            ).exists()
        ).scalar()
    
    @staticmethod
    def crear_pago(datos):
        nuevo_cobro = Cobro(
            usuario_plataforma_id=datos["usuario_plataforma_id"],
            comprobante_id=None,
            mes_anio=datos["mes_anio"],
            monto_deuda=datos["monto_deuda"],
            estado=datos["estado"]
        )
        db.session.add(nuevo_cobro)

        return nuevo_cobro
    
    @staticmethod
    def desvincular_pagos_pendientes(up_id):
        db.session.query(Cobro).filter_by(
            usuario_plataforma_id=up_id,
            estado='pendiente'
        ).delete(synchronize_session=False)
        db.session.flush()

    @staticmethod
    def borrado_total_por_ids(vinculos_ids):
        """Borra físicamente los cobros vinculados a los usuarios provistos"""
        return db.session.query(Cobro).filter(
            Cobro.usuario_plataforma_id.in_(vinculos_ids)
        ).delete(synchronize_session=False)
    
    @staticmethod
    def actualizar_monto_cobros(lista_up_ids, nuevo_monto):
        if not lista_up_ids or nuevo_monto is None:
            return False

        flash(
            f"IDs obtenidos: {', '.join(map(str, lista_up_ids))}",
            "info"
        )

        # Actualiza usando la columna que conecta al contrato
        filas = db.session.query(Cobro).filter(
            Cobro.usuario_plataforma_id.in_(lista_up_ids),
            Cobro.estado == 'pendiente'
        ).update({Cobro.monto_deuda: float(nuevo_monto)}, synchronize_session=False)

        flash(f"Registros actualizados: {filas}")
        db.session.flush()
        db.session.commit()
        return True
    
