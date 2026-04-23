# ===================================================================================================
# seed_admin.py
# ===================================================================================================
from app import create_app
from app.core.db_manager import db
from app.core.models import Usuario
# ===================================================================================================
def seed_admin():
    app = create_app()
    # ===================================================================================================
    with app.app_context():
        print("🌱 Iniciando seeder de Administrador...")

        # 1. Verificar si el administrador ya existe por su teléfono
        admin_existente = Usuario.query.filter_by(telefono='7774399424').first()
        
        if not admin_existente:
            # 2. Crear la instancia del Administrador
            nuevo_admin = Usuario(
                nombres='AXEL',
                apeP='NAVA',
                apeM='SANCHEZ',
                telefono='7774399424',
                rol='admin'
            )
            
            try:
                # 3. Guardar en la base de datos
                db.session.add(nuevo_admin)
                db.session.commit()
                print(f"✅ Administrador {nuevo_admin.nombres} creado con éxito.")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error al crear el admin: {e}")
        else:
            print("⚠️ El administrador con ese teléfono ya existe en la base de datos.")

if __name__ == '__main__':
    seed_admin()