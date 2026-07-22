from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from contextlib import contextmanager

# Instancia global del ORM
db = SQLAlchemy()

class ManagerDB:
    def __init__(self, app=None, fresh=False):
        if app:
            self.init_app(app, fresh)

    def init_app(self, app, fresh=False):
        """Inicializa la app y sincroniza los modelos con la DB."""
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        
        if fresh:
            self.restart_db(db_uri)
        
        db.init_app(app)

        with app.app_context():
            # Es vital importar los modelos antes de create_all() 
            # para que el ORM los registre.
            import app.core.models            
            db.create_all()
            print("✅ ManagerDB: Modelos ORM sincronizados correctamente.")

    def restart_db(self, uri):
            """Lógica para resetear la base de datos física."""
            # Dividimos la URL para obtener el servidor y el nombre de la DB
            # Ejemplo: 'mysql+pymysql://user:pass@localhost/mi_db'
            base_uri, db_name = uri.rsplit('/', 1)
            
            # Limpiamos el nombre por si tiene parámetros (ej. ?charset=utf8mb4)
            db_name = db_name.split('?')[0]

            # Conectamos a la base de datos del sistema para poder borrar la nuestra
            # En MySQL/MariaDB se suele dejar vacío después del slash
            engine = create_engine(f"{base_uri}/") 
            
            with engine.connect() as conn:
                # Finalizamos cualquier transacción activa para poder borrar
                conn.execute(text("COMMIT")) 
                conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"⚠️ ManagerDB: Base de datos '{db_name}' recreada.")
    @contextmanager
    def transaction(self):
        """
        Manejador de contexto para transacciones ORM.
        Uso: 
        with manager.transaction() as session:
            session.add(nuevo_objeto)
        """
        try:
            yield db.session
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ ManagerDB: Error detectado, rollback ejecutado: {e}")
            raise e
        finally:
            # Cerramos la sesión para evitar fugas de memoria
            db.session.remove()