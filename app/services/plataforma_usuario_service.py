# app/services/plataforma_usuario_service.py
# ===================================================================================================
from app.core.models.plataforma_usuario import PlataformaUsuario
from app import db
from datetime import datetime, date
# ===================================================================================================
class PlataformaUsuarioService:
    @staticmethod
    def obtener_plataformas_de_usuario(usuario_id):
        if not usuario_id:
            return []

        # queremos los servicios que usa actualmente.
        resultados = db.session.query(PlataformaUsuario.id).filter_by(
            usuario_id=int(usuario_id),
            activo=1 
        ).all()

        # Desempaquetamos las tuplas en una lista limpia de Python
        return [id_vinculo for (id_vinculo,) in resultados]
# ===================================================================================================
    @staticmethod
    def vincular_plataformas_a_usuario(usuario_id, ids_a_agregar):
        """Activa relaciones existentes (activo=0 -> activo=1) o crea nuevas si no existen"""
        if not ids_a_agregar:
            return
        
        fecha_hoy = datetime.now().date()
        vinculos_actuales = db.session.query(PlataformaUsuario).filter_by(
            usuario_id=usuario_id
        ).all()
        mapa_vinculos = {v.plataforma_id: v for v in vinculos_actuales}

        for p_id in ids_a_agregar:
            p_id_int = int(p_id)

            vinculo_existente = mapa_vinculos.get(p_id_int)
            
            if vinculo_existente:
                vinculo_existente.activo = 1
                vinculo_existente.fecha_ingreso = fecha_hoy
            else:
                nuevo_vinculo = PlataformaUsuario(
                    usuario_id=usuario_id,
                    plataforma_id=p_id_int,
                    activo=1,
                    fecha_ingreso=fecha_hoy
                )
                db.session.add(nuevo_vinculo)
# ===================================================================================================    
    @staticmethod
    def desvincular_plataformas_de_usuario(usuario_id, id_plataformas):
        """Desactiva múltiples relaciones (Borrado Lógico) cambiando activo a 0"""
        if not id_plataformas:
            return False
            
        # Ejecuta un solo UPDATE masivo en MariaDB: 
        db.session.query(PlataformaUsuario).filter(
            PlataformaUsuario.usuario_id == usuario_id,
            PlataformaUsuario.plataforma_id.in_(id_plataformas)
        ).update({PlataformaUsuario.activo: 0}, synchronize_session=False)
        
        return True
# ===================================================================================================
    @staticmethod
    def obtener_vinculos_de_plataforma(plataforma_id):
        """Retorna una lista con los IDs de la plataform_usuario."""
        if not plataforma_id:
            return []

        resultados = db.session.query(PlataformaUsuario.id).filter_by(
            plataforma_id=int(plataforma_id)
        ).all()

        return [id_vinculo for (id_vinculo,) in resultados]
# ===================================================================================================
    @staticmethod
    def desvincular_usuarios_de_plataforma(plataforma_id):
        """Borra los registros de plataforma_user asociados a la plataforma"""
        return db.session.query(PlataformaUsuario).filter(
            PlataformaUsuario.plataforma_id == plataforma_id
        ).delete(synchronize_session=False) # Cambiado a False por velocidad en cascada
# ===================================================================================================
