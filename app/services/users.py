from flask import current_app

class UserService:
    def __init__(self):
        # Accedemos al manager que ya vive en la app
        self.db = current_app.db

    def buscar_usuario(self, tel=None, user_id=None, nombre=None):
        """Busca un usuario por teléfono, ID o Nombre."""
        if user_id:
            sql = """SELECT u.*, p.nombre AS plataforma FROM users u 
                LEFT JOIN plataforma_user pu ON pu.user_id = u.id
                LEFT JOIN plataformas p ON pu.plataforma_id = p.id WHERE u.id = %s
            """
            params = (user_id,)
            mode = 'one'
        elif tel:
            sql = """SELECT u.*, p.nombre AS plataforma FROM users u 
                LEFT JOIN plataforma_user pu ON pu.user_id = u.id
                LEFT JOIN plataformas p ON pu.plataforma_id = p.id WHERE u.telefono = %s
            """
            params = (tel,)
            mode = 'one'
        elif nombre:
            # Usamos LIKE para búsquedas parciales por nombre
            sql = """SELECT u.*, p.nombre AS plataforma FROM users u 
                LEFT JOIN plataforma_user pu ON pu.user_id = u.id
                LEFT JOIN plataformas p ON pu.plataforma_id = p.id WHERE u.nombres LIKE %s
            """
            params = (f"%{nombre}%",)
            mode = 'all' # Cambiamos a 'all' porque puede haber varios con el mismo nombre
        else:
            return None
        
        return self.db.execute(sql, params, mode=mode)
    
    
    def obtener_usuarios(self, search_query=None, plataforma_id=None):
        # Usamos la estructura que ya te funcionó en cobros
        sql = """
            SELECT u.*, p.nombre AS plataforma, p.id AS p_id FROM 
                users u
            JOIN plataforma_user pu ON u.id = pu.user_id
            JOIN plataformas p ON pu.plataforma_id = p.id
            WHERE 1=1
        """
        params = []

        # Buscador (Nombres o Teléfono)
        if search_query:
            # IMPORTANTE: Cambié 'u.nombre' por 'u.nombres' y 'u.apeP' como en tu borrador
            sql += " AND (u.nombres LIKE %s OR u.apeP LIKE %s OR u.apeM LIKE %s OR u.telefono LIKE %s)"
            busqueda = f"%{search_query.strip()}%"
            params.extend([busqueda, busqueda, busqueda, busqueda])

        # Filtro de Plataforma
        if plataforma_id and plataforma_id != '':
            sql += " AND p.id = %s"
            params.append(plataforma_id)

        sql += " ORDER BY u.id DESC"

        # Debug por si acaso (puedes verlo en tu terminal de Arch)
        # print(f"QUERY: {sql} | PARAMS: {params}")

        resultados = self.db.execute(sql, params, mode='all')
        return resultados if resultados is not None else []
    
    def crear_usuario(self, datos):
        sql = """
            INSERT INTO users (nombres, apeP, apeM, telefono, rol)
            VALUES (%s, %s, %s, %s, %s);
        """
        
        params = [
            datos['nombres'],
            datos['apeP'],
            datos['apeM'],
            datos['telefono'],
            'no_admin'
        ]

        return self.db.execute(sql, params)
    
    def actualizar_usuario(self, user_id, datos):
        sql = """
            UPDATE users 
            SET nombres = %s, apeP = %s, apeM = %s, telefono = %s 
            WHERE id = %s
        """
        params = [
            datos['nombres'],
            datos['apeP'],
            datos['apeM'],
            datos['telefono'],
            user_id
        ]
        # Tu execute devolverá el número de filas afectadas
        return self.db.execute(sql, params)
    
    def eliminar_usuario(self, user_id):
            try:
                # Al borrar al usuario, la DB borra en cascada 
                # plataforma_user y cobros automáticamente.
                sql = "DELETE FROM users WHERE id = %s"
                res = self.db.execute(sql, (user_id,))
                
                return res # Devolverá 1 (filas afectadas) si tuvo éxito
            except Exception as e:
                print(f"❌ Error al eliminar usuario: {e}")
                return None