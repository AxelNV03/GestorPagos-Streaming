# ===================================================================================================
# app/core/models/usuario.py
# ===================================================================================================
from app.core.db_manager import db
from datetime import datetime
# ===================================================================================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apeP = db.Column(db.String(100), nullable=False)
    apeM = db.Column(db.String(100), nullable=True) # Opcional según tu SQL    
    telefono = db.Column(db.String(20), unique=True, nullable=False)    
    rol = db.Column(
        db.Enum('admin', 'no_admin', name='rol_usuarios_enum'), 
        default='no_admin'
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # ===================================================================================================
    # Relación con la tabla intermedia para saber en qué plataformas está el usuario
    suscripciones = db.relationship('PlataformaUsuario', backref='perfil_usuario', lazy=True)    
    # Relación con los comprobantes que el usuario ha subido
    comprobantes = db.relationship('Comprobante', backref='emisor', lazy=True)
    # ===================================================================================================
    def __repr__(self):
        return f'<Usuario {self.nombres} {self.apeP} ({self.telefono})>'