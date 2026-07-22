# ===================================================================================================
# app/core/models/plataforma.py
# ===================================================================================================
from app.core.db_manager import db
from sqlalchemy import Computed
import math
# ===================================================================================================
class Plataforma(db.Model):
    __tablename__ = 'plataformas'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)
    cuota = db.Column(db.Numeric(10, 2), nullable=True)
    dia_cobro = db.Column(db.Integer, default=1)
    url_logo = db.Column(db.String(255), default='default_logo.png')
    correo_admin = db.Column(db.String(255), nullable=False)
    max_cupos = db.Column(db.Integer, default=5)
    # ===================================================================================================
    # Relación: Una plataforma tiene muchos registros de usuarios
    usuarios_vinculados = db.relationship('PlataformaUsuario', backref='plataforma', lazy=True)
    # ===================================================================================================
    @property
    def total_usuarios(self):
        """
        Calcula el número de usuarios actualmente vinculados a esta plataforma.
        Usa la relación 'usuarios_vinculados' definida arriba.
        """
        return len(self.usuarios_vinculados)

    @property
    def cupos_disponibles(self):
        """
        Resta el total de usuarios actuales del máximo de cupos permitidos.
        Útil para saber si aún se pueden agregar personas a la cuenta.
        """
        return self.max_cupos - self.total_usuarios

    @property
    def tiene_cupos(self):
        """ Indica con un booleano si aun hay cupos """
        return self.cupos_disponibles > 0
    # ===================================================================================================
    def __repr__(self):
        return f'<Plataforma {self.nombre} - ${self.precio_total}>'