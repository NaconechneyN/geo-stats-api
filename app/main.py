import json
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, database

# Crear las tablas automáticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Global GeoStats API",
    description="API de datos geográficos con análisis estadístico SQL",
    version="1.0.0"
)

# --- ENDPOINT 1: ETL OFFLINE (Lectura de archivo local) ---
@app.post("/etl/populate-db", status_code=201)
def populate_database(db: Session = Depends(database.get_db)):
    """
    IMPORTACIÓN OFFLINE: Lee el archivo 'countries.json' local y llena la base de datos.
    """
    # 1. Verificamos si ya hay datos
    if db.query(models.Country).count() > 0:
        return {"message": "La base de datos ya tiene información. Borra el archivo .db si quieres recargar."}

    print("Iniciando carga desde archivo local...")

    # 2. Leer archivo JSON local
    file_path = "countries.json"
    
    if not os.path.exists(file_path):
        return {"error": f"No se encontró el archivo '{file_path}' en la carpeta raíz. Asegúrate de haberlo creado."}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            countries_data = json.load(f)
        print(f"Archivo leído. Total elementos: {len(countries_data)}")
    except Exception as e:
        return {"error": f"Error leyendo el JSON: {str(e)}"}

    # 3. Transformar y Guardar (ETL)
    count = 0
    errores = 0
    
    for c in countries_data:
        try:
            name = c.get("name", {}).get("common", "Unknown")
            # Manejo de listas vacías
            continents_list = c.get("continents", [])
            continent = continents_list[0] if continents_list else "Unknown"
            
            capital_list = c.get("capital", [])
            capital = capital_list[0] if capital_list else "N/A"
            
            country = models.Country(
                name=name,
                continent=continent,
                capital=capital,
                population=c.get("population", 0),
                area_sq_km=c.get("area", 0.0),
                region=c.get("region", "Unknown"),
                flag_emoji=c.get("flag", "")
            )
            db.add(country)
            count += 1
        except Exception as e:
            print(f"Error procesando {name}: {e}")
            errores += 1
            continue

    db.commit()
    return {
        "message": "Carga manual exitosa.",
        "importados": count,
        "fallidos": errores
    }


# --- ENDPOINT 2: Listar con Filtros ---
@app.get("/countries/", response_model=list[schemas.CountryResponse])
def read_countries(continent: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    query = db.query(models.Country)
    if continent:
        query = query.filter(models.Country.continent == continent)
    
    countries = query.offset(skip).limit(limit).all()
    
    # Calculamos la densidad al vuelo
    for c in countries:
        if c.area_sq_km and c.area_sq_km > 0:
            c.population_density = round(c.population / c.area_sq_km, 2)
        else:
            c.population_density = 0
            
    return countries


# --- ENDPOINT 3: Estadísticas SQL ---
@app.get("/stats/continent-summary")
def get_continent_stats(db: Session = Depends(database.get_db)):
    stats = db.query(
        models.Country.continent,
        func.count(models.Country.id).label("total_countries"),
        func.sum(models.Country.population).label("total_population"),
        func.avg(models.Country.area_sq_km).label("avg_area")
    ).group_by(models.Country.continent).all()

    return [
        {
            "continent": s.continent,
            "countries_count": s.total_countries,
            "total_population": s.total_population,
            "average_area_sq_km": round(s.avg_area, 2) if s.avg_area else 0
        } 
        for s in stats
    ]