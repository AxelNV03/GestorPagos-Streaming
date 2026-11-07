#!/bin/bash
# /app/recordatorio_vencido.sh

cd /app
python -c "
from app import create_app
from app.services.email_service import EmailService
from app.services.periodo_service import PeriodoService
from app.services.usuario_service import UsuarioService
from app.services.cobro_service import CobroService

app = create_app()
with app.app_context():
    info_p = PeriodoService.obtener_periodo_actual()
    usuarios = UsuarioService.obtener_todos()
    
    for u in usuarios:
        if not u.correo:
            continue
        
        cobros = CobroService.cobros_del_mes(u.id, info_p['mes'], info_p['anio'])
        pendientes = [c for c in cobros if c['estado'] == 'pendiente']
        
        if not pendientes:
            continue
        
        total = sum(c['monto'] for c in pendientes)
        plataformas = '<br>'.join([f'{c[\"plataforma\"]}: \${c[\"monto\"]:,.2f}' for c in pendientes])
        
        EmailService.recordatorio_vencido(u, plataformas, total)
        print(f'Enviado a {u.correo}')
"