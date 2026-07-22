# ===================================================================================================
# app/core/models/comprobante.py
# ===================================================================================================
from app.core.db_manager import db
from datetime import datetime
# ===================================================================================================
class Comprobante(db.Model):
    __tablename__ = 'comprobantes'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios.id', ondelete='CASCADE'), 
        nullable=False
    )    
    ruta_archivo = db.Column(db.String(255), nullable=False)
    nota_usuario = db.Column(db.Text, nullable=True)
    motivo_rechazo = db.Column(db.Text, nullable=True)    
    comentario = db.Column(db.Text, nullable=True)
    estado = db.Column(
        db.Enum('revision', 'aprobado', 'rechazado', name='estado_comprobante_enum'), 
        default='revision'
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # ===================================================================================================
    cobros_asociados = db.relationship('Cobro', backref='comprobante_ref', lazy=True)
    usuario = db.relationship('Usuario', back_populates='comprobantes', lazy=True)
    # ===================================================================================================
    def __repr__(self):
        return f'<Comprobante ID: {self.id} | Estado: {self.estado}>'