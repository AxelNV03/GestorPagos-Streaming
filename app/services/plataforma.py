# app/services/plataforma.py
# ===================================================================================================
from app.core.models import Plataforma # Importamos el db y el Modelo directamente
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.core.models.cobro import Cobro
from app.core.db_manager import db, ManagerDB  # Importa el objeto db de SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
# ===================================================================================================
class PlataformaService:
    @staticmethod
    def pendientes_periodo(periodo_id):
        return Plataforma.query.join(PlataformaUsuario).join(Cobro).filter(
            Cobro.periodo_id == periodo_id,
            Cobro.estado == 'pendiente' # O el estado que uses para no pagado
        ).distinct().all()
    
    