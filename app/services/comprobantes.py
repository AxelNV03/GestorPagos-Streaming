import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

class ComprobanteService:
    def __init__(self):
        # Accedemos al manager que ya vive en la app
        self.db = current_app.db

    def save_file(self, archivo, user_id):
        # Ruta de guardado
        base_path = current_app.config['UPLOAD_FOLDER']
        
        folder_name = datetime.now().strftime("%m_%Y")
        ruta_carpeta = os.path.join(base_path, folder_name)
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Renombramos el file
        filename = secure_filename(archivo.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
    
        # 2. Generar el timestamp con el formato: dia-h-m-s
        formato_tiempo = datetime.now().strftime("%d-%H-%M-%S")
    
        # 3. Construir el nombre: user_id-dia-h-m-s.ext
        # Ejemplo resultado: 5-17-16-45-30.jpg
        nombre_seguro = f"{user_id}-{formato_tiempo}.{ext}"

        ruta_destino = os.path.join(ruta_carpeta, nombre_seguro)
        archivo.save(ruta_destino)
    
        # 4. RETORNO PARA LA BASE DE DATOS
        # Retornamos '02_2026/5-17-16-45-30.jpg'
        return os.path.join(folder_name, nombre_seguro)
    
    
    def crear_registro(self, path_file, nota=None):
        sql = """
            INSERT INTO comprobantes (ruta_archivo, nota, monto_abonado)
            VALUES (%s, %s, 0.00)
        """
        params = (
            path_file, 
            nota if nota else 'ninguna'
        )
        return self.db.execute(sql, params)
    
    def actualizar_comprobante(self, nuevo_estado, comprobante_id):
        """
        Actualiza el estado de la imagen del comprobante.
        Valores permitidos: 'revision', 'aprobado', 'rechazado'
        """
        sql = "UPDATE comprobantes SET estado = %s WHERE id = %s"
        self.db.execute(sql, (nuevo_estado, comprobante_id))