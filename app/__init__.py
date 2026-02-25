import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.core.db_manager import db, ManagerDB
from app.routes import register_blueprints

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
    register_blueprints(app)

    @app.context_processor
    def inject_assets():
        """Inyecta automáticamente los CSS según la carpeta del módulo"""
        def get_css_from_folder(folder):
            path = os.path.join(app.root_path, 'static', 'css', folder)
            try:
                return [f for f in os.listdir(path) if f.endswith('.css')]
            except FileNotFoundError:
                return []

        return dict(
            admin_css=get_css_from_folder('admin'),
            user_css=get_css_from_folder('user'),
            auth_css=get_css_from_folder('auth')
        )

    return app

