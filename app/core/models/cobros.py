from app import db

class Cobro(db.Model):
    __tablename__ = 'cobros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Ajuste aquí: debe ser 'plataforma_usuario.id' para coincidir con el __tablename__
    plataforma_usuario_id = db.Column(db.Integer, db.ForeignKey('plataforma_usuario.id', ondelete='CASCADE'), nullable=False)
    
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id', ondelete='CASCADE'), nullable=False)
    comprobante_id = db.Column(db.Integer, db.ForeignKey('comprobantes.id', ondelete='SET NULL'), nullable=True)
    
    estado = db.Column(
        db.Enum('pendiente', 'pagado', 'rechazado', name='estado_cobro'), 
        default='pendiente'
    )
    
    monto = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Cobro ID:{self.id} Monto:{self.monto} Estado:{self.estado}>'