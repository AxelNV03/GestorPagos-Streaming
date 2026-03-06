from app import db

class Cobro(db.Model):
    __tablename__ = 'cobros'
    # ==================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plataforma_usuario_id = db.Column(db.Integer, db.ForeignKey('plataforma_usuario.id', ondelete='CASCADE'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id', ondelete='CASCADE'), nullable=False)
    comprobante_id = db.Column(db.Integer, db.ForeignKey('comprobantes.id', ondelete='SET NULL'), nullable=True)
    estado = db.Column(
        db.Enum('pendiente', 'pagado', 'rechazado', name='estado_cobro'), 
        default='pendiente'
    )    
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    # ==================================================================================================
    # Conexión al periodo (Muchos cobros pertenecen a 1 periodo)
    periodo = db.relationship('Periodo', backref='lista_cobros')
    # Conexión al comprobante (1 cobro tiene 1 comprobante)
    comprobante = db.relationship('Comprobante', backref='cobro', uselist=False)
    # Conexión a la tabla intermedia
    registro_vinculo = db.relationship('PlataformaUsuario', backref='cobros_cliente')
    # ==================================================================================================
    @property
    def usuario(self):
        """Retorna el objeto Usuario dueño de este cobro."""
        return self.registro_vinculo.usuario if self.registro_vinculo else None
    # ==================================================================================================
    @property
    def atrasado(self):
        """Determina si el cobro superó la fecha límite del periodo."""
        from datetime import date
        if self.estado == 'pendiente' and self.periodo:
            return date.today() > self.periodo.limite_pago
        return False
    # ==================================================================================================
    @property
    def estado_color(self):
        """Devuelve la clase de Bootstrap según el estado y si hay atraso."""
        if self.atrasado:
            return "danger" # Rojo si está vencido
        mapa = {
            'pagado': 'success',    # Verde
            'pendiente': 'warning', # Amarillo
            'rechazado': 'secondary'# Gris
        }
        return mapa.get(self.estado, 'dark')
    # ==================================================================================================
    def __repr__(self):
        nombre = self.usuario.nombres if self.usuario else "Sin Usuario"
        return f'<Cobro ID:{self.id} [{nombre}] ${self.monto} ({self.estado})>'