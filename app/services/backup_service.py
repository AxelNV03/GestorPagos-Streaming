# ===================================================================================================
import os
import re  # ← Agregar esto
import subprocess
from datetime import datetime
from flask import current_app
# ===================================================================================================
class BackupService:
    
    @staticmethod
    def generar_backup(nombre=None):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if nombre:
            # Limpiar: sin espacios, solo letras/números/guión bajo
            nombre = re.sub(r'[^a-zA-Z0-9_-]', '_', nombre)
            nombre_final = f"{nombre}_{timestamp}.sql"
        else:
            nombre_final = f"backup_{timestamp}.sql"
        
        ruta = os.path.join(current_app.config['BACKUP_FOLDER'], nombre_final)
        
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        
        cmd = f"mysqldump -u {db_user} -p{db_pass} -h {db_host} {db_name} > {ruta}"
        subprocess.run(cmd, shell=True, check=True)
        
        return nombre_final
# ===================================================================================================
    @staticmethod
    def listar_backups():
        """Lista los backups ordenados por fecha (más reciente primero)"""
        folder = current_app.config['BACKUP_FOLDER']
        backups = []
        for f in os.listdir(folder):
            if f.endswith('.sql'):
                ruta = os.path.join(folder, f)
                size = os.path.getsize(ruta)
                fecha = datetime.fromtimestamp(os.path.getmtime(ruta))
                backups.append({
                    'nombre': f,
                    'fecha': fecha.strftime('%d/%m/%Y - %H:%M'),
                    'size': f"{size / 1024:.1f} KB"
                })
        backups.sort(key=lambda x: x['fecha'], reverse=True)
        return backups
# ===================================================================================================
    @staticmethod
    def eliminar_backup(nombre):
        """Elimina un archivo de backup"""
        ruta = os.path.join(current_app.config['BACKUP_FOLDER'], nombre)
        if os.path.exists(ruta):
            os.remove(ruta)
# ===================================================================================================
    @staticmethod
    def restaurar_backup(archivo):
        """Restaura la BD desde un archivo .sql subido"""
        ruta_temp = os.path.join(current_app.config['BACKUP_FOLDER'], 'restore_temp.sql')
        archivo.save(ruta_temp)
        
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        
        cmd = f"mysql -u {db_user} -p{db_pass} -h {db_host} {db_name} < {ruta_temp}"
        subprocess.run(cmd, shell=True, check=True)
        
        os.remove(ruta_temp)
# ===================================================================================================
    @staticmethod
    def restaurar_desde_archivo(nombre):
        ruta = os.path.join(current_app.config['BACKUP_FOLDER'], nombre)
        if not os.path.exists(ruta):
            raise ValueError('Backup no encontrado')

        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')

        cmd = f"mysql -u {db_user} -p{db_pass} -h {db_host} {db_name} < {ruta}"
        subprocess.run(cmd, shell=True, check=True)