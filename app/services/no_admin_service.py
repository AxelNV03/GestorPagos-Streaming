# app/services/no_admin_service.py
# ===================================================================================================
from flask import session
from datetime import datetime, date
from app.services.periodo_service import PeriodoService
from app.services.cobro_service import CobroService
from app.services.usuario_service import UsuarioService
from app.core.models.comprobante import Comprobante
from app.core.models.cobro import Cobro
from app import db
# ===================================================================================================
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
            'cuota': float(s.plataforma.cuota),
            'correo': s.correo_plataforma or ''
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
# ===================================================================================================
    @staticmethod
    def historial_data(mes=None, anio=None):
        u_id = session.get('user_id')
        
        if not mes or not anio:
            info_p = PeriodoService.obtener_periodo_actual()
            mes = info_p['mes']
            anio = info_p['anio']
        
        mes = int(mes)
        anio = int(anio)
        
        # Navegación
        if mes == 1:
            mes_anterior, anio_anterior = 12, anio - 1
        else:
            mes_anterior, anio_anterior = mes - 1, anio
        
        if mes == 12:
            mes_siguiente, anio_siguiente = 1, anio + 1
        else:
            mes_siguiente, anio_siguiente = mes + 1, anio
        
        MESES_ES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        
        cobros = CobroService.obtener_cobros_usuario(u_id)
        
        # Filtrar solo el mes solicitado
        fecha_filtro = date(anio, mes, 1)
        cobros_mes = [c for c in cobros if c.mes_anio == fecha_filtro]
        
        historial = []
        for c in cobros_mes:
            comp = c.comprobante_ref
            historial.append({
                'id': c.id,
                'plataforma': c.suscripcion.plataforma.nombre,
                'motivo': c.motivo or 'Mensualidad',
                'monto': float(c.monto_deuda),
                'estado': c.estado,
                'mes_anio': c.mes_anio.strftime('%B %Y') if c.mes_anio else '',
                'fecha_subida': comp.created_at.strftime('%d/%m/%Y') if comp else None,
                'comprobante_id': c.comprobante_id,
                'ruta_archivo': comp.ruta_archivo if comp else None,
                'comprobante_estado': comp.estado if comp else None
            })

        historial.sort(key=lambda x: (0 if x['estado'] == 'pendiente' else 1, x['mes_anio']))

        # Comprobantes rechazados del mes
        inicio_mes = datetime(anio, mes, 1)
        if mes == 12:
            fin_mes = datetime(anio + 1, 1, 1)
        else:
            fin_mes = datetime(anio, mes + 1, 1)
        
        comprobantes_rechazados = Comprobante.query.filter(
            Comprobante.usuario_id == u_id,
            Comprobante.estado == 'rechazado',
            Comprobante.created_at >= inicio_mes,
            Comprobante.created_at < fin_mes
        ).order_by(Comprobante.created_at.desc()).all()
        
        rechazados = [{
            'id': c.id,
            'fecha': c.created_at.strftime('%d/%m/%Y'),
            'motivo_rechazo': c.motivo_rechazo or 'Sin motivo',
            'nota': c.nota_usuario or '',
            'ruta_archivo': c.ruta_archivo
        } for c in comprobantes_rechazados]

        # Comprobantes en revisión del mes
        comprobantes_revision = Comprobante.query.filter(
            Comprobante.usuario_id == u_id,
            Comprobante.estado == 'revision',
            Comprobante.created_at >= inicio_mes,
            Comprobante.created_at < fin_mes
        ).order_by(Comprobante.created_at.desc()).all()

        en_revision = [{
            'id': c.id,
            'fecha': c.created_at.strftime('%d/%m/%Y'),
            'nota': c.nota_usuario or '',
            'ruta_archivo': c.ruta_archivo
        } for c in comprobantes_revision]
    
        return {
            'historial': historial,
            'rechazados': rechazados,
            'en_revision': en_revision,
            'label': f"{MESES_ES[mes-1]} {anio}",
            'mes_actual': mes,
            'anio_actual': anio,
            'mes_anterior': mes_anterior,
            'anio_anterior': anio_anterior,
            'mes_siguiente': mes_siguiente,
            'anio_siguiente': anio_siguiente
        }
# ===================================================================================================
    @staticmethod
    def ver_recibo_data(cobro_id):
        cobro = db.session.get(Cobro, cobro_id)
        if not cobro:
            raise ValueError('Cobro no encontrado')
        
        comp = cobro.comprobante_ref
        
        if not comp:
            raise ValueError('Este cobro no tiene comprobante asociado')
        
        return {
            'id': cobro.id,
            'comprobante_id': comp.id if comp else None,
            'plataforma': cobro.suscripcion.plataforma.nombre,
            'motivo': cobro.motivo or 'Mensualidad',
            'monto': float(cobro.monto_deuda),
            'estado': cobro.estado,
            'mes_anio': cobro.mes_anio.strftime('%B %Y') if cobro.mes_anio else '',
            'fecha_subida': comp.created_at.strftime('%d/%m/%Y') if comp else None,
            'ruta_archivo': comp.ruta_archivo if comp else None,
            'comprobante_estado': comp.estado if comp else None,
            'comentario': comp.comentario if comp else None,
            'nota': comp.nota_usuario if comp else None,
            'motivo_rechazo': comp.motivo_rechazo if comp else None
        }
# ===================================================================================================    
    @staticmethod
    def ver_comprobante_data(comprobante_id):
        comp = db.session.get(Comprobante, comprobante_id)
        if not comp:
            raise ValueError('Comprobante no encontrado')
        
        return {
            'id': comp.id,
            'plataforma': 'Comprobante',
            'motivo': comp.nota_usuario or 'Sin nota',
            'monto': 0,
            'estado': 'pendiente',
            'mes_anio': comp.created_at.strftime('%B %Y'),
            'fecha_subida': comp.created_at.strftime('%d/%m/%Y'),
            'ruta_archivo': comp.ruta_archivo,
            'comprobante_estado': comp.estado,  # ← Usar el estado real
            'nota': comp.nota_usuario,
            'motivo_rechazo': comp.motivo_rechazo,
            'comprobante_id': comp.id
        }
# ===================================================================================================
