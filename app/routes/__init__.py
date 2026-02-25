# app/routes/__init__.py

# Importamos los Blueprints de cada archivo de la carpeta routes
from .main import main_bp
from .admin_routes import admin_bp
from .user_routes import user_bp

# Aquí irás agregando los demás conforme los crees, por ejemplo:
# from .admin import admin_bp
# from .pagos import pagos_bp

all_blueprints = [
    main_bp,
    admin_bp,
    user_bp
]