# ===================================================================================================
# app/core/models/plataforma_usuario.py
# ===================================================================================================
from app.core.db_manager import db
from datetime import date
# ===================================================================================================
class PlataformaUsuario(db.Model):
    __tablename__ = 'plataforma_usuario'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    plataforma_id = db.Column(db.Integer, db.ForeignKey('plataformas.id', ondelete='CASCADE'), nullable=False)    
    fecha_ingreso = db.Column(db.Date, default=date.today)
    activo = db.Column(db.Boolean, default=True)
    correo_plataforma = db.Column(db.String(255), nullable=True)  # ← NUEVO
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'plataforma_id', name='uq_usuario_plataforma'),
    )
    # ===================================================================================================
    cobros = db.relationship('Cobro', backref='suscripcion', lazy=True, cascade="all, delete-orphan")
    # ===================================================================================================
    def __repr__(self):
        return f'<PlataformaUsuario ID: {self.id} | User: {self.usuario_id} | Plat: {self.plataforma_id}>'