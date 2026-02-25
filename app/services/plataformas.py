from flask import current_app

class PlataformaService:
    def __init__(self):
        # Accedemos al manager que ya vive en la app
        self.db = current_app.db

    # def conteo_pagos():
    def recaudacion_plataformas(self, mes, anio):
        sql="""
            SELECT * FROM vista_recaudacion_detallada WHERE mes = %s AND anio = %s;
        """
        res = self.db.execute(sql, (mes,anio), mode='all')
        
        
        # Diccionario para mapear el número al nombre
        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        
        #. Inyectamos la lógica de negocio manualmente
        for fila in res:
            total = fila['total_users']
            pagaron = fila['pagaron']
            monto_mensual = float(fila['precio_mensual'])
            num_mes = fila['mes']
            

            # Inyectamos el nombre del mes
            fila['nombre_mes'] = meses_es.get(num_mes, "Desconocido")

            # Cálculos manuales
            fila['restantes'] = total - pagaron
            
            if total > 0:
                fila['recaudado'] = round((monto_mensual / total) * pagaron, 2)
                fila['faltante'] = round(monto_mensual - fila['recaudado'], 2)
            else:
                fila['recaudado'] = 0.0
                fila['faltante'] = monto_mensual

        return res if res is not None else []
    
    def plataformas_restantes_mes(self, mes, anio):
        sql = """
            SELECT * FROM vista_recaudacion_detallada WHERE mes = %s AND anio = %s AND pagaron < total_users;
        """
        res = self.db.execute(sql, (mes, anio), mode='all')
        return res if res is not None else []
        
    def crear_plataforma(self, datos):
        sql = """
            INSERT INTO plataformas (nombre, precio_mensual, dia_cobro, correo_asociado, url_plataforma, url_logo)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (
            datos['nombre'],
            datos['precio_mensual'],
            datos['dia_cobro'],
            datos['correo_asociado'],
            datos['url_plataforma'],
            datos['url_logo']
        )

        return self.db.execute(sql, params)

    def actualizar_plataforma(self, p_id, datos):
        sql = """
            UPDATE plataformas
                SET nombre = %s, precio_mensual = %s, dia_cobro = %s, correo_asociado = %s, url_plataforma = %s, url_logo = %s
            WHERE id = %s;
        """

        params = (
            datos['nombre'],
            datos['precio_mensual'],
            datos['dia_cobro'],
            datos['correo_asociado'],
            datos['url_plataforma'],
            datos['url_logo'],
            p_id  # <--- Este es el %s del WHERE
        )

        return self.db.execute(sql, params)

    def eliminar_plataforma(self, p_id):
        sql = "DELETE FROM plataformas WHERE id = %s"
        return self.db.execute(sql, (p_id,))
    
    def lista_plataformas(self):
        return self.db.execute("SELECT p.*, (SELECT COUNT(*) FROM plataforma_user WHERE plataforma_id = p.id) AS total_users FROM plataformas p", mode='all')
    
    def datos_plataforma(self, p_id):
        sql = """
            SELECT p.*, (SELECT COUNT(*) FROM plataforma_user WHERE plataforma_id = p.id) AS total_users FROM plataformas p WHERE id=%s
        """
        return self.db.execute(sql, (p_id,), mode='one')


    def vincular_user_plataforma(self, user_id, plataforma_id):
        sql = """
            INSERT INTO plataforma_user (user_id, plataforma_id)
            VALUES (%s, %s)
        """
        params = (user_id, plataforma_id)
        return self.db.execute(sql, params)
