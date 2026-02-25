# app/routes/__init__.py
# ===================================================================================================
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
# from app.routes.user import user_bp # Descomenta cuando crees la carpeta user
# ===================================================================================================

def register_blueprints(app):
    """
    Registra todos los Blueprints de la aplicación.
    Aquí definimos los prefijos de URL de manera centralizada.
    """
    
    # 1. Autenticación (Login, Logout)
    # Sin prefijo ('/') para que el login sea la página de entrada
    app.register_blueprint(auth_bp, url_prefix='/')

    # 2. Administración
    # Todas las rutas dentro de admin (dashboard, usuarios, etc.) heredarán '/admin'
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 3. Usuario / Cliente
    # app.register_blueprint(user_bp, url_prefix='/dashboard')
    print("🚀 Rutas: Blueprints registrados correctamente.")