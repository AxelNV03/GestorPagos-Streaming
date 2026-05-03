from flask import Blueprint

# 1. Definimos el Blueprint que agrupa todo
user_bp = Blueprint('user', __name__)

# 2. Importamos las rutas específicas (esto evita problemas de importación circular)
from . import dashboard