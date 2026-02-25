from app.core.models import Usuario
from app.core.db_manager import manager_db

# Instancia de manager para tener acceso al contexto de transacciones
m_db = manager_db()

class UserService:
    
    @staticmethod
    def buscar_usuario(tel=None, user_id=None, nombre=None):
        """Busca un usuario por teléfono, ID o Nombre (incluyendo su plataforma)."""
        query = Usuario.query
        
        if user_id:
            return query.get(user_id) # Retorna objeto o None
        
        if tel:
            return query.filter_by(telefono=tel).first()
        
        if nombre:
            # Retorna una lista con búsqueda parcial (ilike == case insensitive)
            return query.filter(Usuario.nombres.ilike(f"%{nombre}%")).all()
        
        return None
    
    