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
    
    @staticmethod
    def _procesar_y_guardar_logo(p_id, archivo_logo):
        """Método de apoyo para procesar y guardar físicamente el logo en el servidor."""
        if not archivo_logo or archivo_logo.filename == '':
            return None
            
        nombre_seguro = secure_filename(archivo_logo.filename)
        nombre_final = f"{p_id}_{nombre_seguro}"
        ruta_completa = os.path.join(current_app.config['UPLOAD_LOGOS'], nombre_final)
        
        archivo_logo.save(ruta_completa)
        return nombre_final

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

        # Usamos el método de apoyo
        nombre_logo = PlataformaService._procesar_y_guardar_logo(nueva_p.id, archivo_logo)
        if nombre_logo:
            nueva_p.url_logo = nombre_logo

        db.session.commit()
        return nueva_p
    
    @staticmethod
    def editar_plataforma(p_id, datos, archivo_logo):
        p = Plataforma.query.get_or_404(p_id)

        p.nombre = datos.get('nombre')
        p.precio_total = datos.get('precio_total')
        p.dia_cobro = datos.get('dia_cobro')
        p.cuota = datos.get('cuota') 
        p.correo_admin = datos.get('correo_admin')

        db.session.flush()

        # Si viene un nuevo logo, lo procesamos
        if archivo_logo and archivo_logo.filename != '':
            # 1. Borramos el logo anterior
            if p.url_logo:
                ruta_anterior = os.path.join(current_app.config['UPLOAD_LOGOS'], p.url_logo)
                if os.path.exists(ruta_anterior):
                    try:
                        os.remove(ruta_anterior)
                    except OSError:
                        pass

            # 2. Guardamos el nuevo usando el método de apoyo
            p.url_logo = PlataformaService._procesar_y_guardar_logo(p.id, archivo_logo)
        
        db.session.commit()
        return p
    
    @staticmethod
    def eliminar_archivo_logo(p_id):
        """Busca la plataforma y borra su archivo de logo del almacenamiento"""
        p = Plataforma.query.get_or_404(p_id)
        if p.url_logo and p.url_logo != 'default_logo.png': # Evitamos borrar el logo por defecto
            ruta_logo = os.path.join(current_app.config['UPLOAD_LOGOS'], p.url_logo)
            if os.path.exists(ruta_logo):
                try:
                    os.remove(ruta_logo)
                except OSError:
                    pass
        return True

    @staticmethod
    def eliminar_registro_base(p_id):
        """Remueve la plataforma de la sesión (sin hacer commit aún)"""
        p = Plataforma.query.get_or_404(p_id)
        db.session.delete(p)
        return True
    