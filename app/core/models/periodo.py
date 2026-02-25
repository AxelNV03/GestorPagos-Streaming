from app import db
from sqlalchemy import CheckConstraint, UniqueConstraint

class Periodo(db.Model):
    __tablename__ = 'periodos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mes = db.Column(db.Integer, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    limite_pago = db.Column(db.Date, nullable=False)

    # Definimos las restricciones a nivel de tabla (como en SQL)
    __table_args__ = (
        CheckConstraint('mes >= 1 AND mes <= 12', name='check_mes_rango'),
        UniqueConstraint('mes', 'anio', name='pago_unico_periodo'),
    )

    def __repr__(self):
        return f'<Periodo {self.mes}/{self.anio}>'