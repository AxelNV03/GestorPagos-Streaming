# app/services/usuario_service.py
# ===================================================================================================
from sqlalchemy import or_
from app.core.models.usuario import Usuario
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.services.cobro_service import CobroService

from app.core.db_manager import db
from app import db
from sqlalchemy.exc import IntegrityError
# ===================================================================================================
class UsuarioService:
    @staticmethod
    def obtener_todos():
        return Usuario.query.filter(Usuario.rol != "admin").all()
# ===================================================================================================
    @staticmethod
    def buscar_por_id(user_id):
        """Busca un usuario por su clave primaria. Retorna un objeto o None."""
        if not user_id:
            return None
        return db.session.get(Usuario, user_id)
# ===================================================================================================
    @staticmethod
    def buscar_por_telefono(telefono):
        """Búsqueda exacta por teléfono para el Login. Retorna un objeto o None."""
        if not telefono:
            return None
            
        term = str(telefono).strip()
        # Usamos filter para asegurar una comparación limpia contra el modelo
        return db.session.query(Usuario).filter(Usuario.telefono == term).first()
# ===================================================================================================
    @staticmethod
    def filtrar_usuarios(busqueda=None, plataforma_id=None):
        query = db.session.query(Usuario).filter(Usuario.rol != 'admin')
        if plataforma_id and str(plataforma_id).strip():
            query = query.join(PlataformaUsuario).filter(
                PlataformaUsuario.plataforma_id == int(plataforma_id)
            )

        if busqueda and str(busqueda).strip():
            search_term = f"%{busqueda.strip()}%"
            query = query.filter(
                or_(
                    Usuario.nombres.ilike(search_term),
                    Usuario.apeP.ilike(search_term),
                    Usuario.apeM.ilike(search_term),
                    Usuario.telefono.ilike(search_term),
                    Usuario.correo.ilike(search_term)
                )
            )

        query = query.order_by(Usuario.nombres.asc())

        return query.all()    
# ===================================================================================================
    @staticmethod
    def nuevo_usuario(datos):
        nuevo_u = Usuario(
            nombres=datos.get('nombres').upper(),
            apeP=datos.get('apeP').upper(),
            apeM=datos.get('apeM').upper(),
            telefono=datos.get('telefono'),
            correo=datos.get('correo').lower()
        )
        db.session.add(nuevo_u)
        db.session.flush()
        return nuevo_u
# ===================================================================================================
    @staticmethod
    def editar_usuario(usuario_id, datos):
        u = db.session.get(Usuario, usuario_id)
        if not u:
            raise Exception("El usuario que intentas editar no existe.")
        
        # Actualizar los campos básicos
        u.nombres = datos.get('nombres').upper()
        u.apeP = datos.get('apeP').upper()
        u.apeM = datos.get('apeM').upper()
        u.telefono = datos.get('telefono')
        u.correo = datos.get('correo').lower()

        db.session.flush()        
        return u
# ===================================================================================================
    @staticmethod
    def eliminar_usuario(u_id):
        u = Usuario.query.get_or_404(u_id)
        if not u:
            raise Exception("El usuario que intentas eliminar no existe.")
        
        # Primero borramos todas las plataformas vinculadas
        PlataformaUsuario.query.filter(PlataformaUsuario.usuario_id == u.id).delete(synchronize_session=False)

        db.session.delete(u)
        db.session.commit()
        return True
# ===================================================================================================