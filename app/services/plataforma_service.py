# app/services/plataforma_service.py
# ===================================================================================================
import os
from flask import current_app
from app import db
from app.core.models.plataforma import Plataforma
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.core.models.cobro import Cobro
from werkzeug.utils import secure_filename
from sqlalchemy import func
# ===================================================================================================
class PlataformaService:    
    @staticmethod
    def obtener_todas():
        """Retorna una lista con todas las plataformas registradas."""
        return Plataforma.query.all()
# ===================================================================================================
    @staticmethod
    def _procesar_y_guardar_logo(p_id, archivo_logo):
        if not archivo_logo or archivo_logo.filename == '':
            return None
            
        nombre_seguro = secure_filename(archivo_logo.filename)
        nombre_final = f"{p_id}_{nombre_seguro}"
        ruta_completa = os.path.join(current_app.config['UPLOAD_LOGOS'], nombre_final)
        
        archivo_logo.save(ruta_completa)
        return nombre_final
# ===================================================================================================    
    @staticmethod
    def eliminar_archivo_logo(p): 
        if p.url_logo and p.url_logo != 'default_logo.png':
            ruta_logo = os.path.join(current_app.config['UPLOAD_LOGOS'], p.url_logo)
            if os.path.exists(ruta_logo):
                try:
                    os.remove(ruta_logo)
                except OSError:
                    pass # Si el sistema operativo bloquea el archivo, no quebramos el flujo
        return True
# ===================================================================================================
    @staticmethod
    def nueva_plataforma(datos, archivo_logo):
        nueva_p = Plataforma(
            nombre=datos.get('nombre'),
            precio_total=datos.get('precio_total'),
            dia_cobro=datos.get('dia_cobro'),
            cuota=datos.get('cuota'),
            correo_admin=datos.get('correo_admin')
        )        
        db.session.add(nueva_p)
        db.session.flush()


        nombre_logo = PlataformaService._procesar_y_guardar_logo(nueva_p.id, archivo_logo)
        if nombre_logo:
            nueva_p.url_logo = nombre_logo


        return nueva_p
# ===================================================================================================
    @staticmethod
    def editar_plataforma(plataforma, datos, archivo_logo):
        
        plataforma.nombre = datos.get('nombre')
        plataforma.precio_total = datos.get('precio_total')
        plataforma.dia_cobro = datos.get('dia_cobro')
        plataforma.cuota = datos.get('cuota') 
        plataforma.correo_admin = datos.get('correo_admin')
        db.session.flush()

        if archivo_logo and archivo_logo.filename != '':
            PlataformaService.eliminar_archivo_logo(plataforma)
            plataforma.url_logo = PlataformaService._procesar_y_guardar_logo(plataforma.id, archivo_logo)
        
        return plataforma
# ===================================================================================================
    @staticmethod
    def eliminar_plataforma_db(plataforma): # 🚀 Recibe el objeto 'p' directamente
        db.session.delete(plataforma)
# ===================================================================================================