from flask import Flask
import os
from .core.db_manager import ManagerDB
from dotenv import load_dotenv # <--- Agregar esto
from .routes import all_blueprints 

def create_app():
    load_dotenv() # <--- Cargar variables al inicio
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'storage', 'comprobantes')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inyectar os al contexto de Jinja2 correctamente
    @app.context_processor
    def inject_os():
        return {'os': os}

    # Crear instancia DB usando variables de entorno
    app.db = ManagerDB(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        fresh=False
    )
    
    # Registro dinámico
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app