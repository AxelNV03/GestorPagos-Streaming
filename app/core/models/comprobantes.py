from app import db
from datetime import date

class Comprobante(db.Model):
    __tablename__ = 'comprobantes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Enum con nombre para consistencia en MariaDB
    estado = db.Column(
        db.Enum('revision', 'aprobado', 'rechazado', name='estado_comprobante'), 
        default='revision'
    )
    
    ruta_archivo = db.Column(db.String(255), nullable=False)
    nota = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f'<Comprobante ID:{self.id} Estado:{self.estado}>'