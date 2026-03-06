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

    @property
    def es_valido(self):
        """Un chequeo rápido para saber si ya pasó la revisión."""
        return self.estado == 'aprobado'
    
    @property
    def es_rechazado(self):
        """Un chequeo rápido para saber si ya pasó la revisión."""
        return self.estado == 'rechazado'

    @property
    def usuario(self):
        """Retorna el objeto Usuario dueño de este ticket."""
        if self.cobro and self.cobro.registro_vinculo:
            return self.cobro.registro_vinculo.usuario
        return None
    
    @property
    def fecha_formateada(self):
        """Retorna la fecha en formato DD/MM/YYYY."""
        return self.fecha_creacion.strftime('%d/%m/%Y') if self.fecha_creacion else "S/N"
    
    @property
    def estado_color(self):
        mapa = {'revision': 'warning', 'aprobado': 'success', 'rechazado': 'danger'}
        return mapa.get(self.estado, 'secondary')

    def __repr__(self):
        return f'<Comprobante ID:{self.id} Estado:{self.estado}>'