import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    
    @staticmethod
    def _base_template(titulo, contenido, boton_texto=None, boton_url=None):
        boton = f'''
        <a href="{boton_url}" style="display:inline-block;padding:12px 24px;background:#1a1a1a;color:#fff;text-decoration:none;border-radius:8px;font-weight:600;">
            {boton_texto}
        </a>
        ''' if boton_texto else ''
        
        wsp_numero = os.getenv('ADMIN_WHATSAPP', '527774399424')
        
        return f'''
        <div style="max-width:480px;margin:0 auto;font-family:Arial,sans-serif;background:#fff;border-radius:12px;overflow:hidden;border:1px solid #e5e7eb;">
            <div style="background:#1a1a1a;padding:20px;text-align:center;">
                <h1 style="color:#fff;margin:0;font-size:18px;">GestorPagos</h1>
            </div>
            <div style="padding:24px;">
                <h2 style="color:#1a1a1a;margin:0 0 16px;">{titulo}</h2>
                <div style="color:#4a5568;font-size:15px;line-height:1.6;">
                    {contenido}
                </div>
                <div style="margin-top:16px;">
                    {boton}
                    <a href="https://wa.me/{wsp_numero}" style="display:inline-block;padding:12px 24px;background:#1a1a1a;color:#fff;text-decoration:none;border-radius:8px;font-weight:600;margin-left:8px;">
                        💬 WhatsApp
                    </a>
                </div>
            </div>
            <div style="background:#f8f9fa;padding:16px;text-align:center;font-size:12px;color:#8E959B;">
                GestorPagos · pagos.axelnava.com
            </div>
        </div>
        '''
    @staticmethod
    def enviar(destinatario, asunto, mensaje_html):
        try:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('MAIL_FROM')
            msg['To'] = destinatario
            msg['Subject'] = asunto
            msg.attach(MIMEText(mensaje_html, 'html'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error email: {e}")
            return False

    @staticmethod
    def comprobante_recibido(usuario):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"¡Hola {nombre}! 👋"
        contenido = """
        <p>Este correo es para confirmar que recib&iacute; tu comprobante.</p>
        <p>Est&aacute; en <strong>revisi&oacute;n</strong>, te avisar&eacute; cuando sea aprobado.</p>
        <p style='color:#8E959B;font-size:13px;margin-top:16px;'>Si no reconoces este envío, contáctame por WhatsApp.</p>
        """
        return EmailService.enviar(
            usuario.correo,
            "Comprobante recibido - GestorPagos",
            EmailService._base_template(titulo, contenido, "Ver historial", "https://pagos.axelnava.com/user/historial")
        )

    @staticmethod
    def comprobante_aprobado(usuario, cobros_cubiertos, total_cubierto, pendientes_restantes, comentario=None):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"¡Aprobado, {nombre}! ✅"
        
        # Desglose de cobros cubiertos
        desglose = '<br>'.join([f'{c["plataforma"]}: ${c["monto"]:,.2f} - {c["motivo"]}' for c in cobros_cubiertos])
        
        if pendientes_restantes == 0:
            estado = "<p>Todos tus servicios est&aacute;n al d&iacute;a. ¡Gracias por tu pago!</p>"
        else:
            estado = f"<p>A&uacute;n tienes <strong>{pendientes_restantes}</strong> cobros pendientes este mes.</p>"
        
        comentario_html = f"<p style='color:#8E959B;font-size:13px;margin-top:16px;'><strong>Comentario:</strong> {comentario}</p>" if comentario else "<p style='color:#8E959B;font-size:13px;margin-top:16px;'><strong>Comentario:</strong> N/A</p>"
        
        contenido = f"""
        <p>Tu comprobante fue <strong>APROBADO</strong>. Este comprobante cubri&oacute;:</p>
        <p style='background:#f8f9fa;padding:12px;border-radius:8px;'>{desglose}</p>
        <p><strong>Total cubierto: ${total_cubierto:,.2f} MXN</strong></p>
        {estado}
        {comentario_html}
        <p style='color:#8E959B;font-size:13px;margin-top:16px;'>Puedes consultar tu historial en el bot&oacute;n de abajo.</p>
        """
        return EmailService.enviar(
            usuario.correo,
            "Comprobante aprobado - GestorPagos",
            EmailService._base_template(titulo, contenido, "Ver historial", "https://pagos.axelnava.com/user/historial")
        )
    
    @staticmethod
    def comprobante_rechazado(usuario, motivo):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"Comprobante rechazado, {nombre} ❌"
        contenido = f"""
        <p>Tu comprobante fue <strong>RECHAZADO</strong>.</p>
        <p><strong>Motivo:</strong> {motivo}</p>
        <p>Revisa el historial y vuelve a intentarlo. Si tienes dudas, escr&iacute;beme al WhatsApp.</p>
        """
        return EmailService.enviar(
            usuario.correo,
            "Comprobante rechazado - GestorPagos",
            EmailService._base_template(titulo, contenido, "Ver historial", "https://pagos.axelnava.com/user/historial")
        )
    
    @staticmethod
    def comprobante_aprobado(usuario, cobros_cubiertos, total_cubierto, pendientes_restantes, comentario=None):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"¡Aprobado, {nombre}! ✅"
        
        # Desglose de cobros cubiertos
        desglose = '<br>'.join([f'{c["motivo"]}: ${c["monto"]:,.2f}' for c in cobros_cubiertos])        

        if not pendientes_restantes:
            estado = "<p>Todos tus servicios est&aacute;n al d&iacute;a. ¡Gracias por tu pago!</p>"
        else:
            # Desglose de pendientes
            pendientes_html = '<br>'.join([f'{p["motivo"]}: ${p["monto"]:,.2f}' for p in pendientes_restantes])
            estado = f"""
            <p>A&uacute;n tienes cobros pendientes este mes:</p>
            <p style='background:#fef2f2;padding:12px;border-radius:8px;border-left:4px solid #dc3545;'>{pendientes_html}</p>
            <p><strong>Total pendiente: ${sum(p['monto'] for p in pendientes_restantes):,.2f} MXN</strong></p>
            """
        
        comentario_html = f"<p style='color:#8E959B;font-size:13px;margin-top:16px;'><strong>Comentario:</strong> {comentario}</p>" if comentario else "<p style='color:#8E959B;font-size:13px;margin-top:16px;'><strong>Comentario:</strong> N/A</p>"
        
        contenido = f"""
        <p>Tu comprobante fue <strong>APROBADO</strong>. Este comprobante cubri&oacute;:</p>
        <p style='background:#f8f9fa;padding:12px;border-radius:8px;'>{desglose}</p>
        <p><strong>Total cubierto: ${total_cubierto:,.2f} MXN</strong></p>
        {estado}
        {comentario_html}
        <p style='color:#8E959B;font-size:13px;margin-top:16px;'>Puedes consultar tu historial en el bot&oacute;n de abajo.</p>
        """
        return EmailService.enviar(
            usuario.correo,
            "Comprobante aprobado - GestorPagos",
            EmailService._base_template(titulo, contenido, "Ver historial", "https://pagos.axelnava.com/user/historial")
        )

    @staticmethod
    def recordatorio_vencido(usuario, plataformas, total):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"⚠️ Pagos vencidos, {nombre}"
        contenido = f"<p>Tienes pagos <strong>VENCIDOS</strong>:</p><p style='background:#fef2f2;padding:12px;border-radius:8px;border-left:4px solid #dc3545;'>{plataformas}</p><p><strong>Total: ${total:,.2f} MXN</strong></p><p>Evita la suspensión de tus servicios.</p>"
        return EmailService.enviar(
            usuario.correo,
            "⚠️ Pagos vencidos - GestorPagos",
            EmailService._base_template(titulo, contenido, "Subir comprobante", "https://pagos.axelnava.com/user/pago")
        )

    @staticmethod
    def bienvenida(usuario):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"¡Bienvenido, {nombre}! 🎉"
        contenido = """
        <p>Esta es mi plataforma de <strong>Gesti&oacute;n de Pagos</strong>.</p>
        <p>Aqu&iacute; podr&aacute;s:</p>
        <ul>
            <li>Ver todos tus servicios y cuotas</li>
            <li>Revisar cu&aacute;nto pagas cada mes</li>
            <li>Subir tus comprobantes de pago</li>
        </ul>
        <p>Adem&aacute;s, por este medio te enviar&eacute; notificaciones cuando subas un comprobante, cuando sea revisado, y recordatorios mensuales para que no se te pase ninguna fecha.</p>
        <p>Cualquier duda, escr&iacute;beme sin problema.</p>
        <p>&iexcl;Gracias y bienvenido! &#128588;</p>
        """
        return EmailService.enviar(
            usuario.correo,
            "Bienvenido - GestorPagos",
            EmailService._base_template(titulo, contenido, "Panel del Sistema", "https://pagos.axelnava.com/user/dashboard")
        )


    @staticmethod
    def aviso_general(usuario, mensaje, boton_texto=None, boton_url=None):
        nombre = f"{usuario.nombres} {usuario.apeP}"
        titulo = f"Aviso, {nombre} 📢"
        return EmailService.enviar(
            usuario.correo,
            "Aviso - GestorPagos",
            EmailService._base_template(titulo, f"<p>{mensaje}</p>", boton_texto, boton_url)
        )