#!/bin/bash
# /app/scripts/container/alerta_morosos.sh
# Uso: DIA_ENV=3 alerta_morosos.sh  |  DIA_ENV=5 alerta_morosos.sh

cd /app
python -c "
import os
from app import create_app
from app.services.telegram_bot_service import BotService
from app.services.periodo_service import PeriodoService
from app.services.usuario_service import UsuarioService
from app.services.cobro_service import CobroService

app = create_app()
with app.app_context():
    info_p = PeriodoService.obtener_periodo_actual()
    usuarios = UsuarioService.obtener_todos()
    
    morosos = []
    for u in usuarios:
        cobros = CobroService.cobros_del_mes(u.id, info_p['mes'], info_p['anio'])
        pendientes = [c for c in cobros if c['estado'] == 'pendiente']
        
        if not pendientes:
            continue
        
        telefono = (u.telefono or '').strip()
        if telefono and not telefono.startswith('52') and len(telefono) == 10:
            telefono = '52' + telefono
        
        morosos.append({
            'nombre': f'{u.nombres} {u.apeP}',
            'telefono': telefono,
            'plataforma': pendientes[0]['plataforma']  # solo la primera
        })
    
    # Sin morosos → mensaje positivo
    if not morosos:
        BotService.notificar_admin(
            f'🎉 *Todos al día* — {info_p[\"label\"]}\n\nNingún usuario tiene pagos pendientes este mes.'
        )
        print('Sin morosos')
        exit()
    
    # Título según el día
    dia = os.getenv('DIA_ENV', '3')
    if dia == '5':
        titulo = f'⚠️ *Último día para pagar* — {info_p[\"label\"]}'
    else:
        titulo = f'📋 *Cobros pendientes* — {info_p[\"label\"]}'
    
    # Construir mensaje
    texto = f'{titulo}\n'
    texto += f'Usuarios faltos de pago: {len(morosos)}\n\n'
    
    for i, m in enumerate(morosos, 1):
        texto += f'No. {i}\n'
        texto += f'{m[\"nombre\"]} — {m[\"plataforma\"]}\n\n'
    
    # Botones (nombre + apellido)
    botones = []
    for i, m in enumerate(morosos, 1):
        if m['telefono']:
            botones.append([{
                'text': f'💬 {i}. {m[\"nombre\"]}',
                'url': f'https://wa.me/{m[\"telefono\"]}'
            }])
    BotService.notificar_admin(texto, botones if botones else None)
    print(f'Enviado: {len(morosos)} morosos')
"