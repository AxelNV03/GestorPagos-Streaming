from app import db
from sqlalchemy import CheckConstraint, UniqueConstraint

class Periodo(db.Model):
    __tablename__ = 'periodos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mes = db.Column(db.Integer, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    limite_pago = db.Column(db.Date, nullable=False)

    # Relacion Cobros
    cobros = db.relationship('Cobro', backref='periodo_detalle')

    # Definimos las restricciones a nivel de tabla (como en SQL)
    __table_args__ = (
        CheckConstraint('mes >= 1 AND mes <= 12', name='check_mes_rango'),
        UniqueConstraint('mes', 'anio', name='pago_unico_periodo'),
    )

    @property
    def nombre_mes(self):
        """Traduce el número de mes a texto."""
        meses = [None, "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        return meses[self.mes] if 0 < self.mes <= 12 else "Desconocido"

    @property
    def label(self):
        """Ideal para títulos y selectores (Ej: 'Febrero 2026')."""
        return f"{self.nombre_mes} {self.anio}"
    
    @property

    def es_pasado(self):
        """Indica si el periodo ya terminó (mes anterior al actual)."""
        from datetime import date
        hoy = date.today()
        if self.anio < hoy.year: return True
        return self.anio == hoy.year and self.mes < hoy.month

    @property
    
    def es_actual(self):
        """Verifica si es el periodo en curso."""
        from datetime import date
        hoy = date.today()
        return self.mes == hoy.month and self.anio == hoy.year

    @property
    def total_recaudado(self):
        """Suma de todos los cobros pagados en este periodo."""
        # Gracias a la relación 'cobros' que definiste:
        return sum(float(c.monto) for c in self.cobros if c.estado == 'pagado')

    @property
    def total_pendiente(self):
        """Lo que falta por cobrar en este periodo."""
        return sum(float(c.monto) for c in self.cobros if c.estado == 'pendiente')

    def __repr__(self):
        return f'<Periodo {self.label} (ID: {self.id})>'