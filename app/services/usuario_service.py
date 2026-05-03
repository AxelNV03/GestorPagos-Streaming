from sqlalchemy import or_
from app.core.models.usuario import Usuario
from app import db

class UsuarioService:
    @staticmethod
    def buscar_usuario(busqueda=None, user_id=None, exacto=False):
        # 1. Búsqueda por ID (Equivalente al find de Laravel)

        if user_id is not None:
            return db.session.get(Usuario, user_id)

        if not busqueda:
            return None

        term = str(busqueda).strip()
        
        # 2. BÚSQUEDA PARA LOGIN (Exacta)
        if exacto:
            # Usamos db.session.query para ser explícitos
            return db.session.query(Usuario).filter_by(telefono=term).first()

        # 3. BÚSQUEDA PARA ADMIN (Parcial / Filtro)
        search = f"%{term}%"
        return db.session.query(Usuario).filter(
            or_(
                Usuario.telefono.ilike(search),
                Usuario.nombres.ilike(search),
                Usuario.apeP.ilike(search),
                Usuario.apeM.ilike(search)
            )
        ).all()