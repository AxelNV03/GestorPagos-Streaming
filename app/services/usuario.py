# app/services/usuario.py
# ===================================================================================================
from app.core.models import Usuario # Importamos el db y el Modelo directamente
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.core.db_manager import db, ManagerDB  # Importa el objeto db de SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
# ===================================================================================================
class UsuarioService:
    @staticmethod
    def buscar_usuario(busqueda=None, user_id=None):
            """
            Lógica de búsqueda:
            1. Si hay user_id: Busca coincidencia exacta por Llave Primaria.
            2. Si hay busqueda: Busca coincidencias parciales en Teléfono y Nombres.
            """
            # 1. Búsqueda directa (ID no entra en el buscador de texto)
            if user_id:
                return Usuario.query.get(user_id)

            # 2. Si no hay búsqueda ni ID, regresamos lista vacía
            if not busqueda:
                return None            
            # 3. Limpieza del término de búsqueda
            search = f"%{str(busqueda).strip()}%"

            # 4. Búsqueda por texto con ILIKE (Case Insensitive)
            return Usuario.query.filter(
                or_(
                    Usuario.telefono.ilike(search),
                    Usuario.nombres.ilike(search),
                    Usuario.apeP.ilike(search),
                    Usuario.apeM.ilike(search)
                )
            ).first()
    # ===================================================================================================
    @staticmethod
    def obtener_usuarios(search_query=None, plataforma_id=None):
        # 1. Consulta base
        query = Usuario.query

        # 2. Búsqueda por texto
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

        # 3. Filtro de plataforma (CORREGIDO)
        if plataforma_id:
            # Unimos con la tabla nexo usando el nombre de la relación en el modelo Usuario
            query = query.join(PlataformaUsuario).filter(
                PlataformaUsuario.plataforma_id == plataforma_id
            )

        # 4. Orden y ejecución
        return query.order_by(Usuario.id.desc()).all()
    # ===================================================================================================
    def crear_usuario(datos):
        try:
            nuevo_usuario = Usuario(
                nombres=datos.get('nombres'),
                apeP=datos.get('apeP'),
                apeM=datos.get('apeM'),
                telefono=datos.get('telefono'),
                rol='no_admin'
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return nuevo_usuario
        except IntegrityError:
            db.session.rollback() # ¡Vital! Si falla, hay que limpiar la sesión
            return None # O lanza una excepción personalizada: "El teléfono ya existe"
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