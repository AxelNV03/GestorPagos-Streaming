from app.core.models.cobro import Cobro
from app.core.models.plataforma_usuario import PlataformaUsuario
from datetime import date
from app import db
from sqlalchemy import func, or_

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
        """ Obtiene el total de pagos realizados vs usuarios totales del periodo. """
        total_usuarios = db.session.query(func.count(PlataformaUsuario.id)).scalar() or 0
        fecha_filtro = date(anio, int(mes), 1)
        pagos_realizados  = db.session.query(func.count(Cobro.id)).filter(
            Cobro.mes_anio == fecha_filtro,
            Cobro.estado == 'pagado'
        ).scalar() or 0

        return {
            "pagos": pagos_realizados,
            "users": total_usuarios
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