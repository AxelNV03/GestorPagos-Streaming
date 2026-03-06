from app import db

class Plataforma(db.Model):
    __tablename__ = 'plataformas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_mensual = db.Column(db.Numeric(10, 2), nullable=False)
    dia_cobro = db.Column(db.Integer, default=1)
    url_logo = db.Column(db.String(255), nullable=True)
    correo_asociado = db.Column(db.String(255), nullable=True)

    # Para saber qué usuarios tiene
    suscripciones = db.relationship('PlataformaUsuario', backref='plataforma')

    @property
    def total_clientes(self):
        return len(self.suscripciones)

    @property
    def ingresos_proyectados(self):
        return self.total_clientes * float(self.precio_mensual)
    
    @property
    def resumen_usuarios(self):
        """Un string rápido para identificar la plataforma y su volumen de clientes."""
        return f"{self.nombre} ({self.total_clientes} clientes)"

    def __repr__(self):
        return f'<Plataforma {self.nombre} [${self.precio_mensual}]>'
    
    
    