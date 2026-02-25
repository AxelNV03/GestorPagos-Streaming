# ===========================================================================================================    
import mysql.connector
import os
from mysql.connector import Error
# ===========================================================================================================    
class ManagerDB:
    """ Adaptador de base de datos. Si fresh=True reinicia la base de datos al iniciar."""
    def __init__(self, host, user, password, database, fresh=False):
        self.db_name = database
        self.config = {
            'host': host,
            'user': user,
            'password': password
        }

        if fresh:
            self.restart_db()
        else:
            self.start_db()
# ===========================================================================================================    
    def connect_server(self):
        """Conecta al servidor MySQL sin seleccionar base de datos."""
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"[ERROR] Conectando al servidor: {e}")
            return None
# ===========================================================================================================    
    def connect_db(self):
        """Conecta directamente a la base de datos del proyecto."""
        try:
            return mysql.connector.connect(**self.config, database=self.db_name)
        except Error as e:
            # 1049 = Unknown database
            if e.errno == 1049:
                print(f"[INFO] Base de datos '{self.db_name}' no encontrada.")

                # Intentar crearla
                if self.start_db():
                    return mysql.connector.connect(**self.config, database=self.db_name, use_pure=True) 
                else:
                    print("[ERROR] No se pudo crear la base de datos.")
                    return None
            else:
                print(f"[ERROR] Conectando a la base de datos: {e}")
                return None
# ===========================================================================================================    
    def start_db(self):
        """Crea la base de datos si no existe y luego crea las tablas."""
        print(f"[INFO] Iniciando creación de la base de datos '{self.db_name}'...")
        conn = self.connect_server()

        if conn is None:
            print("[ERROR] No se pudo establecer conexión con el servidor.")
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}`")
            conn.commit()
            cursor.close()
            print("[OK] Base de datos creada o ya existente.")
        except Error as e:
            print(f"[ERROR] Ejecutando SQL de creación: {e}")
            return False
        finally:
            conn.close()

        # Crear tablas
        return self.start_tables()
# ===========================================================================================================    
    def start_tables(self):
        try:
            # 1. Leer el archivo SQL
            with open('app/core/tablas.sql', 'r') as f:
                sql_script = f.read()
        except FileNotFoundError:
            print("❌ No se encontró el archivo tablas.sql")
            return False

        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # 2. Dividimos el script por punto y coma y ejecutamos una por una
            commands = sql_script.split(';')
            
            for command in commands:
                cmd = command.strip()
                if cmd: # Evitamos ejecutar strings vacíos
                    cursor.execute(cmd)
            
            conn.commit()
            print("✅ Tablas creadas/verificadas con éxito (sentencia por sentencia).")
            return True
        except Exception as e:
            print(f"❌ Error al ejecutar sentencias SQL: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
# ===========================================================================================================    
    def restart_db(self):
        """Borra todo y reconstruye desde cero"""
        print(f"⚠️ Reseteando base de datos '{self.db_name}'...")
        conn = self.connect_server()

        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS `{self.db_name}`")
            conn.commit()
            cursor.close()
            return self.start_db()

        except Error as e:
            print(f"❌ Error en el reset: {e}")
            return False

        finally:
            conn.close()
# ===========================================================================================================
    def execute(self, query, params=None, mode=None): # Cambiamos fetch por mode
        conn = self.connect_db()
        if not conn: return None
        
        try:
            cursor = conn.cursor(dictionary=True, buffered=True) # <--- Agregamos buffered=True
            cursor.execute(query, params or ())
            
            if mode == 'all':
                result = cursor.fetchall()
            elif mode == 'one':
                result = cursor.fetchone()
            else:
                conn.commit()
                result = cursor.lastrowid if cursor.lastrowid and cursor.lastrowid > 0 else cursor.rowcount
                
            cursor.close()
            return result
        except Error as e:
            print(f"❌ Error ejecutando query: {e}")
            return None
        finally:
            conn.close()
# ===========================================================================================================
    def commit(self):
        """Para compatibilidad, aunque tu execute ya hace commit si no es consulta."""
        # Como tu execute actual abre y cierra conexiones, 
        # el commit global es difícil de aplicar sin cambiar todo.
        pass
# ===========================================================================================================
    def rollback(self):
        """Evita el error de AttributeError."""
        print("⚠️ Rollback llamado: Nota que ManagerDB cierra conexiones en cada execute.")
        pass