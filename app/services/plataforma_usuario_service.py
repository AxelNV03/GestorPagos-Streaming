from app.core.models.plataforma_usuario import PlataformaUsuario
from app import db
from datetime import datetime, date

class PlataformaUsuarioService:

    @staticmethod
    def obtener_relacion(u_id, p_id):
        return db.session.query(PlataformaUsuario).filter_by(
            usuario_id=u_id,
            plataforma_id=p_id
        ).first()
    
    @staticmethod
    def vincular_plataformas(u_id, ids_a_agregar):
        """Activa relaciones existentes (activo=0 -> activo=1) o crea nuevas si no existen"""
        if not ids_a_agregar:
            return
            
        for p_id in ids_a_agregar:
            # 🔍 Buscamos si ya existe un registro histórico (activo 0 o 1) para este usuario y plataforma
            vinculo_existente = db.session.query(PlataformaUsuario).filter_by(
                usuario_id=u_id,
                plataforma_id=p_id
            ).first()
            
            if vinculo_existente:
                # 🔄 CAMINO A: Si ya existía, lo reactivamos y actualizamos su fecha al día de hoy
                vinculo_existente.activo = 1
                vinculo_existente.fecha_ingreso = datetime.now().date()
            else:
                # 🆕 CAMINO B: Si es la primera vez que contrata este servicio, lo insertamos desde cero
                nuevo_vinculo = PlataformaUsuario(
                    usuario_id=u_id,
                    plataforma_id=p_id,
                    activo=1,
                    fecha_ingreso=datetime.now().date() # Usa el nombre exacto de tu columna de fecha
                )
                db.session.add(nuevo_vinculo)
        
        # Sincronizamos en memoria para que impacte la transacción actual
        db.session.flush()
    
    @staticmethod
    def desvincular_plataformas(u_id, ids_a_eliminar):
        """Desactiva múltiples relaciones (Borrado Lógico) cambiando activo a 0"""
        if not ids_a_eliminar:
            return False
            
        # Ejecuta un solo UPDATE masivo en MariaDB: 
        # UPDATE plataforma_usuario SET activo = 0 WHERE usuario_id = X AND plataforma_id IN (Y, Z)
        db.session.query(PlataformaUsuario).filter(
            PlataformaUsuario.usuario_id == u_id,
            PlataformaUsuario.plataforma_id.in_(ids_a_eliminar)
        ).update({PlataformaUsuario.activo: 0}, synchronize_session=False)
        
        db.session.flush()
        return True

    @staticmethod
    def obtener_ids_por_plataforma(p_id):
        """Retorna una lista plana de enteros con los IDs de la tabla intermedia"""
        if not p_id:
            return []
            
        # Ejecuta un SELECT id FROM plataforma_usuario WHERE plataforma_id = X
        resultados = db.session.query(PlataformaUsuario.id).filter_by(
            plataforma_id=int(p_id)
        ).all()
        
        # Desenredamos las tuplas que regresa SQLAlchemy [(1,), (2,)] -> [1, 2]
        return [id_pivote for (id_pivote,) in resultados]
    
    @staticmethod
    def eliminar_registros_plataforma(p_id):
        """Borra físicamente los vínculos intermedios de la plataforma"""
        return db.session.query(PlataformaUsuario).filter(
            PlataformaUsuario.plataforma_id == p_id
        ).delete(synchronize_session=False) # Cambiado a False por velocidad en cascada