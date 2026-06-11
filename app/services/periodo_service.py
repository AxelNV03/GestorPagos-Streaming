# app/services/periodo_service.py
# ===================================================================================================
from datetime import datetime, date
# ===================================================================================================
MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
# ===================================================================================================
class PeriodoService:
    @staticmethod
    def obtener_periodo_actual():
        hoy = datetime.now()
        nombre_mes = MESES_ES.get(hoy.month)
        return {
            'id': int(f"{hoy.year}{hoy.month:02d}"),
            'mes': hoy.month,
            'anio': hoy.year,
            'nombre_mes': nombre_mes,
            'label': f"{nombre_mes} {hoy.year}"
        }
# ===================================================================================================   