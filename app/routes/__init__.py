# app/routes/__init__.py
# ===================================================================================================
from app.routes.public.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.user import user_bp
# ===================================================================================================
def register_blueprints(app):    
    # 1. Autenticación (Login, Logout)
    # Sin prefijo ('/') para que el login sea la página de entrada
    app.register_blueprint(auth_bp, url_prefix='/')

    # 2. Administración
    # Todas las rutas dentro de admin
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 3. Usuarios
    # Todas las rutas dentro de user
    app.register_blueprint(user_bp, url_prefix='/user')


    # 4. Usuario / Cliente
    print("🚀 Rutas: Blueprints registrados correctamente.")
# ===================================================================================================