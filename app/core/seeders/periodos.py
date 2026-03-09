from datetime import date
from app.core.db_manager import db
from app.core.models.periodo import Periodo

def seed_periodos_largo_plazo():
    """Genera periodos desde Enero 2026 hasta Diciembre 2040."""
    print("⏳ Iniciando siembra de periodos (2026 - 2040)...")
    
    contador = 0
    for anio in range(2026, 2041):  # De 2026 a 2040
        for mes in range(1, 13):    # De Enero a Diciembre
            
            # Verificamos si ya existe para evitar errores de duplicado
            existente = Periodo.query.filter_by(mes=mes, anio=anio).first()
            
            if not existente:
                # Establecemos fecha límite por defecto: día 10 de cada mes
                fecha_limite = date(anio, mes, 10)
                
                nuevo = Periodo(
                    mes=mes,
                    anio=anio,
                    limite_pago=fecha_limite
                )
                db.session.add(nuevo)
                contador += 1
        
        # Hacemos commit por cada año para no saturar la memoria si fuera una carga masiva
        db.session.commit()
        print(f"✅ Año {anio} completado.")

    print(f"🚀 Proceso terminado. Se crearon {contador} nuevos periodos.")