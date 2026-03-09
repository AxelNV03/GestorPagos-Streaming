# app/services/periodo.py
# ===================================================================================================
from app.core.models import Periodo # Importamos el db y el Modelo directamente
from app.core.db_manager import db  # Importa el objeto db de SQLAlchemy
from datetime import date
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
# ===================================================================================================
class PeriodoService:
    @staticmethod
    def periodo_actual():
        hoy = date.today()

        # UniqueConstraint: solo habrá uno o ninguno
        return Periodo.query.filter_by(mes=hoy.month, anio=hoy.year).first()