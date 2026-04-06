# ===================================================================================================
# app/core/models/plataforma.py
# ===================================================================================================
from app.core.db_manager import db
from sqlalchemy import Computed
# ===================================================================================================
class Plataforma(db.Model):
    __tablename__ = 'plataformas'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)
    cuota_sugerida = db.Column(
        db.Numeric(10, 2), 
        Computed("precio_total / 5", persisted=True)
    )
    dia_cobro = db.Column(db.Integer, default=1)
    url_logo = db.Column(db.String(255), default='default_logo.png')
    correo_admin = db.Column(db.String(255), nullable=False)
    max_cupos = db.Column(db.Integer, default=5)
    # ===================================================================================================
    # Relación: Una plataforma tiene muchos registros de usuarios
    usuarios_vinculados = db.relationship('PlataformaUsuario', backref='plataforma', lazy=True)
    # ===================================================================================================
    def __repr__(self):
        return f'<Plataforma {self.nombre} - ${self.precio_total}>'