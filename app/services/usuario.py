# app/services/user_service.py
# ===================================================================================================
from app.core.models import Usuario # Importamos el db y el Modelo directamente
from app.core.db_manager import db, ManagerDB  # Importa el objeto db de SQLAlchemy
from sqlalchemy import or_
# ===================================================================================================
class UserService:
    @staticmethod
    def buscar_usuario(busqueda=None, user_id=None):
            """
            Lógica de búsqueda:
            1. Si hay user_id: Busca coincidencia exacta por Llave Primaria.
            2. Si hay busqueda: Busca coincidencias parciales en Teléfono y Nombres.
            """
            # 1. Búsqueda directa (ID no entra en el buscador de texto)
            if user_id:
                u = Usuario.query.get(user_id)
                return [u] if u else []

            if not busqueda:
                return []

            term_str = str(busqueda).strip()
            search = f"%{term_str}%"

            # 2. Búsqueda por texto (Nombre, Apellidos y Teléfono únicamente)
            return Usuario.query.filter(
                or_(
                    Usuario.telefono.ilike(search),
                    Usuario.nombres.ilike(search),
                    Usuario.apeP.ilike(search),
                    Usuario.apeM.ilike(search)
                )
            ).all()
    # ===================================================================================================
    @staticmethod
    def obtener_usuarios(search_query=None, plataforma_id=None):
        """
        Consulta usuarios aplicando filtros dinámicos.
        Retorna una lista de objetos Usuario.
        """
        # 1. Iniciamos la consulta base
        query = Usuario.query

        # 2. Si hay búsqueda de texto, aplicamos el OR en nombres, apellidos y teléfono
        if search_query:
            search = f"%{search_query.strip()}%"
            query = query.filter(
                or_(
                    Usuario.nombres.ilike(search),
                    Usuario.apeP.ilike(search),
                    Usuario.apeM.ilike(search),
                    Usuario.telefono.ilike(search)
                )
            )

        # 3. Si hay filtro de plataforma, hacemos el JOIN
        if plataforma_id:
            # SQLAlchemy es inteligente: sabe cómo unir Usuario con Plataforma 
            # a través de tu tabla intermedia 'plataforma_usuario'
            query = query.join(Usuario.plataformas).filter_by(id=plataforma_id)

        # 4. Ordenamos por el más reciente y ejecutamos
        return query.order_by(Usuario.id.desc()).all()
    # ===================================================================================================
    @staticmethod
    def crear_usuario(datos):
        nuevo_usuario = Usuario(
            nombres=datos['nombres'],
            apeP=datos['apeP'],
            apeM=datos.get('apeM'), # .get() por si es opcional
            telefono=datos['telefono'],
            rol='no_admin'
        )
        db.session.add(nuevo_usuario)
        db.session.commit() # ¡Importante! En SQLAlchemy hay que hacer commit
        return nuevo_usuario
    # ===================================================================================================
    @staticmethod
    def eliminar_usuario(user_id):
        user = Usuario.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    # ===================================================================================================