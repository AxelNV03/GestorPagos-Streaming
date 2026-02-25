import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
# Instanciamos las extensiones fuera para evitar importaciones circulares
from app.core.db_manager import db, ManagerDB
from .routes import all_blueprints

migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Configuración de Seguridad y Almacenamiento
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Configurar directorio de almacenamiento 
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'storage', 'comprobantes'))
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


    # Configuración de SQLAlchemy para MariaDB
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de extensiones
    m_db = ManagerDB(app, fresh=False)
    migrate.init_app(app, db)

    # Registro dinámico de Blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app