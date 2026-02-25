from flask import current_app

class CobroService:
    def __init__(self):
        # Accedemos al manager que ya vive en la app
        self.db = current_app.db

    def cobros_mes_especifico(sef):
        sql="""
            SELECT * FROM PAGos
        """
        return True
    
    def recaudacion_global(self, periodo_id):
        sql = """
            SELECT 
                SUM(monto) as total_esperado,
                SUM(CASE WHEN estado = 'pagado' THEN monto ELSE 0 END) as recaudado,
                SUM(CASE WHEN estado = 'pendiente' THEN monto ELSE 0 END) as pendiente
            FROM cobros
            WHERE periodo_id = %s
        """
        return self.db.execute(sql, (periodo_id, ), mode='one')
    
    def conteo_global_users_pagos(self, periodo_id):
        sql = """
            SELECT 
                COUNT(*) as users,
                SUM(CASE WHEN estado = 'pagado' THEN 1 ELSE 0 END) as pagos
            FROM cobros 
            WHERE periodo_id = %s  
        """
    
        # IMPORTANTE: Cambié el return para que ejecute la consulta, no solo devuelva el texto
        res = self.db.execute(sql, (periodo_id,), mode='one')
        
        # Si no hay registros aún, devolvemos ceros para que no rompa el HTML
        if not res or res['users'] is None:
            return {'users': 0, 'pagos': 0}
            
        return res
    
    def actualizar_cobros_pendientes_plataforma(self, plataforma_id, nuevo_precio, total_users):
        if total_users > 0:
            costo_individual = round(float(nuevo_precio) / total_users, 2)
        else:
            costo_individual = nuevo_precio 

        sql = """
            UPDATE cobros c
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
            SET c.monto = %s
            WHERE pu.plataforma_id = %s
            AND c.estado = 'Pendiente'
        """
        params = (costo_individual, plataforma_id)
        
        # IMPORTANTE: Asegúrate de que tu db.execute devuelva el rowcount.
        # Si devuelve None, forzamos que sea 0.
        res = self.db.execute(sql, params)
        return res if res is not None else 0
    
    def crear_cobro(self, pr_id, pu_id, monto):
        sql = """
            INSERT INTO cobros (user_plataforma_id, periodo_id, monto)
            VALUES (%s, %s, %s)
        """
        params = (pu_id, pr_id, monto)
        return self.db.execute(sql, params)
    
    def obtener_cobro(self, cobro_id):
        # Primero defines de dónde sacas los datos (JOIN) y al final filtras (WHERE)
        sql = """
            SELECT c.*, com.ruta_archivo, com.nota, com.created_at AS fecha_subida 
            FROM cobros c 
            LEFT JOIN comprobantes com ON c.comprobante_id = com.id 
            WHERE c.id = %s
        """
        # IMPORTANTE: La coma después de cobro_id convierte esto en una tupla
        params = (cobro_id,) 
        
        # Agregamos mode='one' para que devuelva el registro (el diccionario)
        return self.db.execute(sql, params, mode='one')
    
    def obtener_cobros(self, busqueda=None, mes=None, anio=None, plataforma=None, switch=None, user_id=None):
        sql = """
            SELECT
                c.*,
                CONCAT(u.nombres, ' ', u.apeP) AS usuario, u.nombres as nombre, u.id AS user_id,
                per.mes, per.anio, per.limite_pago,
                com.id AS com_id, com.monto_abonado, com.ruta_archivo, REPLACE(REPLACE(nota, '\n', ' '), '\r', '') as nota,
                com.created_at AS fecha_comprobante,
                p.id AS plat_id, p.nombre AS plataforma
            FROM cobros c
            JOIN periodos per ON c.periodo_id = per.id
            LEFT JOIN comprobantes com ON c.comprobante_id = com.id
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
            JOIN users u ON u.id = pu.user_id
            JOIN plataformas p ON p.id = pu.plataforma_id
            WHERE 1=1
        """

        params = []
        
        if busqueda:
            sql += """ AND (u.nombres LIKE %s OR u.telefono LIKE %s OR u.apeP LIKE %s OR u.apeM LIKE %s )"""
            busqueda = f"%{busqueda.strip()}%"
            params.extend([busqueda, busqueda, busqueda, busqueda])

        if mes:
            sql += " AND per.mes = %s"
            params.append(mes)

        if anio:
            sql += """ AND per.anio = %s"""
            params.append(anio)

        if plataforma:
            sql += """ AND p.id = %s"""
            params.append(plataforma)

        if user_id:
            sql += """ AND u.id = %s"""
            params.append(plataforma)


        if switch == 'revision':
            # En SQL no se usa != NULL, se usa IS NOT NULL
            sql += " AND c.comprobante_id IS NOT NULL AND com.estado = 'revision'"

        # ISNULL(comp.fecha_subida), -- Los NULL se van al final del bloque del mes
        sql += """ 
            ORDER BY per.mes DESC, (com.id IS NULL) DESC, com.created_at DESC
        """

        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        res = self.db.execute(sql, params, mode='all')
        
        if not res:
                return []
                
        for fila in res:
            fila['nombre_mes'] = meses_es.get(fila['mes'], "Desconocido")
        
        return res
    
    def asociar_comprobante(self, comprobante_id, cobro_id):
        try:
            sql_cobro = """
                UPDATE cobros SET comprobante_id = %s WHERE id = %s
            """
            # Ejecutamos la actualización del cobro
            self.db.execute(sql_cobro, (comprobante_id, cobro_id))
            return True
        except Exception as e:
            print(f"Error al asociar: {e}")
            return False

    
    def actualizar_cobro(self, nuevo_estado, cobro_id):
        """
        Actualiza el estado de un registro en la tabla cobros.
        Valores permitidos para nuevo_estado: 'pendiente', 'pagado', 'rechazado'
        """
        sql = "UPDATE cobros SET estado = %s WHERE id = %s"
        # Usamos execute de tu objeto de base de datos
        self.db.execute(sql, (nuevo_estado, cobro_id))
        # No olvides que el commit se hace al final de toda la ruta
    
    def ultimo_cobro(self, user_id, estado):
        sql = """
            SELECT c.*, p.limite_pago, p.mes, p.anio, pu.id AS plataforma_user_id
            FROM cobros c
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id 
            JOIN periodos p ON c.periodo_id = p.id
            WHERE pu.user_id = %s AND estado = %s
            ORDER BY p.limite_pago DESC LIMIT 1
        """
        params = (user_id, estado)
        return self.db.execute(sql, params, mode='one')
    
    def historial_user(self, user_id):
            # 1. Usamos LEFT JOIN en comprobantes para que aparezcan cobros sin ticket aún
            sql = """
                SELECT 
                    c.*,
                    com.created_at AS fecha_pago, 
                    com.nota, com.ruta_archivo,
                    p.nombre AS plataforma_nombre,
                    per.mes, per.anio
                FROM cobros c
                JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
                JOIN plataformas p ON pu.plataforma_id = p.id
                JOIN periodos per ON per.id = c.periodo_id
                JOIN comprobantes com ON com.id = c.comprobante_id 
                WHERE pu.user_id = %s
            """
            # LA COMA ES VITAL: (user_id,) indica que es una tupla de un solo elemento
            params = (user_id,)

            sql += " ORDER BY c.id DESC, per.mes DESC"

            res = self.db.execute(sql, params, mode='all')
            
            # Seguridad extra: si no hay resultados, devolvemos lista vacía
            if not res:
                return []
                
            return res