from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from contextlib import contextmanager

db = SQLAlchemy()

class ManagerDB:
    # Crea una instancia de la conexion a la db
    def __init__(self, app=None, fresh=False):
        if app:
            self.init_app(app, fresh)

    # Crear la base de dato con los models
    def init_app(self, app, fresh=False):
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        if fresh:
            self.restart_db(db_uri)
        
        db.init_app(app)

        with app.app_context():
            import app.core.models            
            db.create_all()
            print("✅ manager_db: Tablas sincronizadas y seguras.")


    def restart_db(self, uri):
        base_uri = uri.rsplit('/', 1)[0]
        db_name = uri.rsplit('/', 1)[1]
        engine = create_engine(base_uri)
        with engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS `{db_name}`"))
            conn.execute(text(f"CREATE DATABASE `{db_name}`"))
            conn.commit()
            print(f"⚠️ manager_db: Base de datos '{db_name}' reseteada.")

    @contextmanager
    def transaction(self):
        """
        Manejador de contexto para transacciones seguras.
        Si algo falla dentro del 'with', hace rollback automáticamente.
        """
        try:
            yield db.session
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en la transacción: {e}")
            raise e # Re-lanzamos para que el service/route sepa que falló
        finally:
            db.session.remove() # Devuelve la conexión al pool de Arch