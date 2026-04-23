# ===================================================================================================
# app/__init__.py
# ===================================================================================================
import os
from flask import Flask
from dotenv import load_dotenv
from app.core.db_manager import db, ManagerDB
from app.routes import register_blueprints

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # --- Configuración de Seguridad y Almacenamiento ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key_123')
    
    # Directorio de comprobantes (Ruta absoluta para evitar fallos en Docker)
    upload_path = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'storage', 'comprobantes'))
    app.config['UPLOAD_FOLDER'] = os.path.abspath(upload_path)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # --- Configuración de SQLAlchemy para MariaDB ---
    # Agregamos charset=utf8mb4 para evitar errores con nombres o caracteres especiales
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Inicialización del Manager (ORM Puro) ---
    # Aquí se ejecutan tus modelos y la creación de tablas
    m_db = ManagerDB(app, fresh=False)

    # --- Registro de Rutas ---
    register_blueprints(app)

    # --- Context Processor para Assets ---
    @app.context_processor
    def inject_assets():
        """Inyecta automáticamente los CSS según la carpeta del módulo"""
        def get_css_from_folder(folder):
            path = os.path.join(app.root_path, 'static', 'css', folder)
            if os.path.exists(path):
                return [f for f in os.listdir(path) if f.endswith('.css')]
            return []

        return dict(
            admin_css=get_css_from_folder('admin'),
            user_css=get_css_from_folder('user'),
            auth_css=get_css_from_folder('auth')
        )

    return app