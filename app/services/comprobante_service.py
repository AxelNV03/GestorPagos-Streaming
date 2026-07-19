# app/services/comprobante_service.py
# ===================================================================================================
from app.core.models.comprobante import Comprobante
from app import db
from datetime import date
import os
import uuid
from datetime import datetime
from flask import current_app
from app.core.models.usuario import Usuario
from werkzeug.utils import secure_filename

from sqlalchemy.orm import joinedload
from sqlalchemy import func
# ===================================================================================================
class ComprobanteService:
    @staticmethod
    def _rango_mes(mes, anio):
        """Devuelve (fecha_inicio, fecha_fin) para cubrir todo el mes"""
        inicio = date(int(anio), int(mes), 1)
        if int(mes) == 12:
            fin = date(int(anio) + 1, 1, 1)
        else:
            fin = date(int(anio), int(mes) + 1, 1)
        return inicio, fin
# ===================================================================================================
    @staticmethod
    def obtener_comprobantes_del_mes(mes, anio, estado=None):
        fecha_inicio, fecha_fin = ComprobanteService._rango_mes(mes, anio)
        
        consulta = db.session.query(Comprobante)\
            .options(
                joinedload(Comprobante.usuario),
                joinedload(Comprobante.cobros_asociados)
            )\
            .filter(Comprobante.created_at >= fecha_inicio)\
            .filter(Comprobante.created_at < fecha_fin)
        
        if estado:
            consulta = consulta.filter(Comprobante.estado == estado)
        
        return consulta.order_by(Comprobante.created_at.desc()).all()
# ===================================================================================================
    @staticmethod
    def metricas_mes(mes, anio):
        fecha_inicio, fecha_fin = ComprobanteService._rango_mes(mes, anio)
        
        resultados = db.session.query(
            Comprobante.estado,
            func.count(Comprobante.id)
        ).filter(
            Comprobante.created_at >= fecha_inicio,
            Comprobante.created_at < fecha_fin
        ).group_by(Comprobante.estado).all()
        
        conteo = dict.fromkeys(['revision', 'aprobado', 'rechazado'], 0)
        conteo.update(resultados)
        return conteo
# ===================================================================================================
    @staticmethod
    def _procesar_y_guardar_archivo(archivo, usuario, comprobante):
        """Guarda el archivo en storage/comprobantes/{usuario_id}/ y retorna el nombre"""
        if not archivo or archivo.filename == '':
            raise ValueError('Debe seleccionar una imagen')
        
        ext = os.path.splitext(archivo.filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise ValueError('Formato no permitido. Use JPG o PNG')
        
        # Nombre: {nombres}_{apeP}_{created_at}_{estado}{ext}
        nombres = secure_filename(f"{usuario.nombres}_{usuario.apeP}").lower()
        fecha = comprobante.created_at.strftime('%Y%m%d_%H%M%S')
        estado = comprobante.estado
        nombre_final = f"{nombres}_{fecha}_{estado}{ext}"
        
        # Ruta: storage/comprobantes/{usuario_id}/
        ruta_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(usuario.id))
        os.makedirs(ruta_dir, exist_ok=True)
        
        ruta_completa = os.path.join(ruta_dir, nombre_final)
        archivo.save(ruta_completa)
        
        # Ruta relativa para la DB
        return f"{usuario.id}/{nombre_final}"
# ===================================================================================================
    @staticmethod
    def guardar_comprobante(usuario_id, archivo, nota):
        """Crea un nuevo comprobante en estado 'revision'"""
        usuario = db.session.get(Usuario, int(usuario_id))
        if not usuario:
            raise ValueError('Usuario no encontrado')
        
        comprobante = Comprobante(
            usuario_id=usuario.id,
            ruta_archivo='',  # temporal
            nota_usuario=nota,
            estado='revision'
        )
        db.session.add(comprobante)
        db.session.flush()  # Para obtener created_at
        
        # Guardar archivo con nombre completo
        nombre_archivo = ComprobanteService._procesar_y_guardar_archivo(archivo, usuario, comprobante)
        comprobante.ruta_archivo = nombre_archivo
        
        db.session.commit()
        return comprobante
# ===================================================================================================
    @staticmethod
    def cambiar_estado(comprobante, nuevo_estado, comentario=None):
        """Cambia el estado del comprobante y renombra el archivo"""
        if nuevo_estado not in ['aprobado', 'rechazado']:
            raise ValueError('Estado no válido')
        
        estado_anterior = comprobante.estado
        ruta_vieja = os.path.join(current_app.config['UPLOAD_FOLDER'], comprobante.ruta_archivo)
        
        # Nuevo nombre
        nombre_actual = os.path.basename(comprobante.ruta_archivo)
        nombre_nuevo = nombre_actual.replace(f"_{estado_anterior}.", f"_{nuevo_estado}.")
        ruta_nueva = os.path.join(os.path.dirname(ruta_vieja), nombre_nuevo)
        
        # Renombrar archivo
        if os.path.exists(ruta_vieja):
            os.rename(ruta_vieja, ruta_nueva)
        
        # Actualizar DB
        comprobante.estado = nuevo_estado
        comprobante.ruta_archivo = comprobante.ruta_archivo.replace(
            f"_{estado_anterior}.", f"_{nuevo_estado}."
        )
        
        if nuevo_estado == 'rechazado':
            comprobante.motivo_rechazo = comentario
        elif comentario:
            comprobante.comentario = comentario
        
        db.session.commit()
# ===================================================================================================