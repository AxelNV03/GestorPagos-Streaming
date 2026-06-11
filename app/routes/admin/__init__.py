from flask import Blueprint

# 1. Definimos el Blueprint que agrupa todo
admin_bp = Blueprint('admin', __name__)

# 2. Importamos las rutas específicas (esto evita problemas de importación circular)
from . import dashboard
from . import plataformas
from . import usuarios
from . import cobros