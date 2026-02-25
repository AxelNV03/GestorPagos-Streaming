from app import create_app

# 1. Creamos la instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # 2. Arrancamos el servidor de desarrollo
    # host='0.0.0.0' permite que otros dispositivos en tu red (como tu cel) vean la app
    # debug=True reinicia el server automáticamente cuando guardas cambios en el código
    app.run(host='0.0.0.0', port=5001, debug=True)