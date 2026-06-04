from sqlalchemy import or_
from app.core.models.usuario import Usuario
from app.core.models.plataforma_usuario import PlataformaUsuario
from app.core.db_manager import db, ManagerDB
from app import db
from sqlalchemy.exc import IntegrityError

class UsuarioService:
    @staticmethod
    def obtener_todos():
        return Usuario.query.filter(Usuario.rol != "admin").all()

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
    def filtrar_usuarios(busqueda=None, plataforma_id=None):
        # 1. INICIO
        query = db.session.query(Usuario).filter(Usuario.rol != 'admin')

        # 2. FILTRO POR PLATAFORMA (Relación Muchos a Muchos):
        if plataforma_id:
            query = query.join(PlataformaUsuario).filter(
                PlataformaUsuario.plataforma_id == plataforma_id
            )

        # 3. FILTRO POR CAMPOS DE TEXTO (Búsqueda General):
        if busqueda:
            # Limpiamos espacios y preparamos el comodín % para SQL LIKE.
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

        # 4. EJECUCIÓN: Se genera el SQL final y se pide la lista de objetos.
        return query.all()
    
    @staticmethod
    def nuevo_usuario(datos):
        nuevo_u = Usuario(
            nombres=datos.get('nombres'),
            apeP=datos.get('apeP'),
            apeM=datos.get('apeM'),
            telefono=datos.get('telefono'),
            correo=datos.get('correo')
        )
        db.session.add(nuevo_u)
        db.session.flush()

        # Vincular plataformas
        plataformas = datos.get('plataformas', [])
        if plataformas:
            for p_id in plataformas:
                vinculo = PlataformaUsuario(
                    usuario_id=nuevo_u.id,
                    plataforma_id=p_id
                )
                db.session.add(vinculo)

        db.session.commit()
        return nuevo_u

