from flask import current_app

class PeriodoService:
    def __init__(self):
        # Accedemos al manager que ya vive en la app
        self.db = current_app.db
    
    def periodo_actual(self):
        sql = """
        SELECT * FROM periodos WHERE anio = YEAR(CURRENT_DATE) AND mes = MONTH(CURRENT_DATE);
        """
        res = self.db.execute(sql, mode='one')

        if not res:
            return None
        
        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        
        }
        res['nombre_mes'] = meses_es.get(res['mes'], "Desconocido")
        return res
