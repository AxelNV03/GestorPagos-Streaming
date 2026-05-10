from sqlalchemy import or_
from app.core.models.usuario import Usuario
from app.core.db_manager import db, ManagerDB
from app import db
from sqlalchemy.exc import IntegrityError

class UsuarioService:
    @staticmethod
    def buscar_por_id(user_id):
        """Busca un usuario por su clave primaria. Retorna un objeto o None."""
        if not user_id:
            return None
        return db.session.get(Usuario, user_id)

    @staticmethod
    def buscar_por_telefono(telefono):
        """Búsqueda exacta por teléfono para el Login. Retorna un objeto o None."""
        if not telefono:
            return None
            
        term = str(telefono).strip()
        # Usamos filter para asegurar una comparación limpia contra el modelo
        return db.session.query(Usuario).filter(Usuario.telefono == term).first()

    @staticmethod
    def filtrar_usuarios(busqueda):
        """Búsqueda parcial para el panel de administración. Retorna una lista."""
        if not busqueda:
            return []

        search = f"%{str(busqueda).strip()}%"
        return db.session.query(Usuario).filter(
            or_(
                Usuario.telefono.ilike(search),
                Usuario.nombres.ilike(search),
                Usuario.apeP.ilike(search),
                Usuario.apeM.ilike(search)
            )
        ).all()
    