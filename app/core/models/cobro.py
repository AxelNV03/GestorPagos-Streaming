# ===================================================================================================
# app/core/models/cobro.py
# ===================================================================================================
from app.core.db_manager import db
from datetime import date
# ===================================================================================================
class Cobro(db.Model):
    __tablename__ = 'cobros'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_plataforma_id = db.Column(
        db.Integer, 
        db.ForeignKey('plataforma_usuario.id', ondelete='CASCADE'), 
        nullable=False
    )    
    comprobante_id = db.Column(
        db.Integer, 
        db.ForeignKey('comprobantes.id', ondelete='SET NULL'), 
        nullable=True
    )    
    mes_anio = db.Column(db.Date, nullable=False)    
    monto_deuda = db.Column(db.Numeric(10, 2), nullable=False)    
    estado = db.Column(
        db.Enum('pendiente', 'en_revision', 'pagado', name='estado_cobro_enum'), 
        default='pendiente'
    )
    # ===================================================================================================
    def __repr__(self):
        return f'<Cobro ID: {self.id} | Deuda: {self.monto_deuda} | Estado: {self.estado}>'