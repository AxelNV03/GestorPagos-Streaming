import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from .routes import all_blueprints

# Instanciamos las extensiones fuera para evitar importaciones circulares
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Configuración de Seguridad y Almacenamiento
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Configurar directorio de almacenamiento 
    env_upload_path = os.getenv('UPLOAD_FOLDER')
    if env_upload_path:
        app.config['UPLOAD_FOLDER'] = env_upload_path
    else:
        app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'storage', 'comprobantes')

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as e:
        print(f"Error creando el directorio: {e}")

    # Configuración de SQLAlchemy para MariaDB
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registro dinámico de Blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app