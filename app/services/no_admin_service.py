# app/services/user_service.py
from flask import session
from datetime import datetime, date
from app.services.periodo_service import PeriodoService
from app.services.cobro_service import CobroService
from app.services.usuario_service import UsuarioService
from app.core.models.comprobante import Comprobante

class NoAdminService:
    @staticmethod
    def dashboard_data():
        u_id = session.get('user_id')
        info_p = PeriodoService.obtener_periodo_actual()
        mes, anio = info_p['mes'], info_p['anio']
        
        usuario = UsuarioService.buscar_por_id(u_id)
        cobros_mes = CobroService.cobros_del_mes(u_id, mes, anio)
        
        total_pendiente = sum(c['monto'] for c in cobros_mes if c['estado'] == 'pendiente')
        total_pagado = sum(c['monto'] for c in cobros_mes if c['estado'] == 'pagado')
        total_pendiente_count = sum(1 for c in cobros_mes if c['estado'] == 'pendiente')
        
        # Comprobantes del mes
        inicio_mes = datetime(int(anio), int(mes), 1)
        if int(mes) == 12:
            fin_mes = datetime(int(anio) + 1, 1, 1)
        else:
            fin_mes = datetime(int(anio), int(mes) + 1, 1)
        
        comprobantes_mes = Comprobante.query.filter(
            Comprobante.usuario_id == u_id,
            Comprobante.created_at >= inicio_mes,
            Comprobante.created_at < fin_mes
        ).all()
        
        comprobante_en_revision = any(c.estado == 'revision' for c in comprobantes_mes)
        comprobante_rechazado = any(c.estado == 'rechazado' for c in comprobantes_mes)
        
        hoy = date.today()
        limite = date(int(anio), int(mes), 5)
        dias_vencido = (hoy - limite).days if hoy > limite else 0
        
        mensualidades_vencidas_count = sum(
            1 for c in cobros_mes 
            if c['estado'] == 'pendiente' 
            and c.get('motivo', '').startswith('Mensualidad')
            and hoy > limite
        )
        
        extras_pendientes_count = sum(
            1 for c in cobros_mes 
            if c['estado'] == 'pendiente' 
            and not c.get('motivo', '').startswith('Mensualidad')
        )
        
        plataformas_activas = sum(1 for s in usuario.suscripciones if s.activo) if usuario.suscripciones else 0
        
        plataformas_lista = [{
            'nombre': s.plataforma.nombre,
            'logo': s.plataforma.url_logo,
            'cuota': float(s.plataforma.cuota)
        } for s in usuario.suscripciones if s.activo]

        return {
            'periodo': info_p,
            'user': usuario,
            'cobros_mes': cobros_mes,
            'total_pendiente': total_pendiente,
            'total_pagado': total_pagado,
            'total_pendiente_count': total_pendiente_count,
            'comprobante_en_revision': comprobante_en_revision,
            'comprobante_rechazado': comprobante_rechazado,
            'dias_vencido': dias_vencido,
            'mensualidades_vencidas_count': mensualidades_vencidas_count,
            'extras_pendientes_count': extras_pendientes_count,
            'plataformas_activas': plataformas_activas,
            'plataformas_lista': plataformas_lista
        }