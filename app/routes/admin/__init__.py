from flask import Blueprint

# 1. Definimos el Blueprint que agrupa todo
admin_bp = Blueprint('admin', __name__)

# 2. Importamos los submódulos (esto registra las rutas en admin_bp)
from . import dashboard
from . import servicios