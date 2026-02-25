from app import db

class Plataforma(db.Model):
    __tablename__ = 'plataformas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_mensual = db.Column(db.Numeric(10, 2), nullable=False)
    dia_cobro = db.Column(db.Integer, default=1)
    url_logo = db.Column(db.String(255), nullable=True)
    correo_asociado = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Plataforma {self.nombre}>'
    
    