# app/services/user_service.py
# ===================================================================================================
from app.core.models import Usuario # Importamos el db y el Modelo directamente
from app.core.db_manager import db, ManagerDB  # Importa el objeto db de SQLAlchemy
# ===================================================================================================

class UserService:
    
    @staticmethod
    def buscar_usuario(tel=None, user_id=None, nombre=None):
        """Busca un usuario por teléfono, ID o Nombre usando SQLAlchemy."""
        query = Usuario.query
        
        if user_id:
            return query.get(user_id) 
        
        if tel:
            return query.filter_by(telefono=tel).first()
        
        if nombre:
            # ilike es Case Insensitive (ignora mayúsculas/minúsculas)
            return query.filter(Usuario.nombres.ilike(f"%{nombre}%")).all()
        
        return None