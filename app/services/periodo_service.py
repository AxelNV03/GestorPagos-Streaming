# app/services/periodo_service.py
from datetime import datetime, date

class PeriodoService:
    @staticmethod
    def obtener_periodo_actual():
        """
        Genera el periodo actual y el objeto de fecha para la base de datos.
        """
        hoy = datetime.now()
        
        # Creamos el objeto date: año, mes, día 1
        # Este objeto es el que se asigna directamente a: cobro.mes_anio
        fecha_db = date(hoy.year, hoy.month, 1)

        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        return {
            'id': int(f"{hoy.year}{hoy.month:02d}"),
            'mes': hoy.month,
            'anio': hoy.year,
            'nombre_mes': meses_es.get(hoy.month),
            'label': f"{meses_es.get(hoy.month)} {hoy.year}"
            # 'fecha_objeto': fecha_db  # <--- Este es el valor para tu columna db.Date
        }

   