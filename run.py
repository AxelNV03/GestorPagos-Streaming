
# ========================================================================================================================
# run.py
# ========================================================================================================================
import os
from app import create_app  # <--- ESTA LÍNEA ES LA QUE FALTA
# 1. Creamos la instancia de la aplicación
app = create_app()

#if __name__ == '__main__':
    # 2. Arrancamos el servidor de desarrollo
#    host='0.0.0.0' # permite que otros dispositivos en tu red (como tu cel) vean la app
#    debug=True # reinicia el server automáticamente cuando guardas cambios en el código
#    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # 2. Arrancamos el servidor con HTTPS
    cert_path = '/app/fullchain.pem'
    key_path = '/app/privkey.pem'
  
    if os.path.exists(cert_path) and os.path.exists(key_path):
        # Con HTTPS
        print("🔐 Iniciando con HTTPS...")
        app.run(host='0.0.0.0', port=5000,
                ssl_context=(cert_path, key_path))
    else:
        # Fallback a HTTP si no hay certificados
        print("⚠️  Certificados no encontrados. Iniciando en HTTP...")
        app.run(host='0.0.0.0', port=5000)
